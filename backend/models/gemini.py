import asyncio
import base64
import time
from typing import Awaitable, Callable, Dict, List
from openai.types.chat import ChatCompletionMessageParam
try:
    from google import genai  # type: ignore
    from google.genai import types  # type: ignore
except ImportError:
    genai = None  # type: ignore
    types = None  # type: ignore
from llm import Completion, Llm
from config import GEMINI_DEFAULT_TIMEOUT, GEMINI_THINKING_TIMEOUT, GEMINI_PREVIEW_TIMEOUT


def extract_image_from_messages(
    messages: List[ChatCompletionMessageParam],
) -> Dict[str, str]:
    """
    Extracts image data from OpenAI-style chat completion messages.

    Args:
        messages: List of ChatCompletionMessageParam containing message content

    Returns:
        Dictionary with mime_type and data keys for the first image found
    """
    for content_part in messages[-1]["content"]:  # type: ignore
        if content_part["type"] == "image_url":  # type: ignore
            image_url = content_part["image_url"]["url"]  # type: ignore
            if image_url.startswith("data:"):  # type: ignore
                # Extract base64 data and mime type for data URLs
                mime_type = image_url.split(";")[0].split(":")[1]  # type: ignore
                base64_data = image_url.split(",")[1]  # type: ignore
                return {"mime_type": mime_type, "data": base64_data}
            else:
                # Handle regular URLs - would need to download and convert to base64
                # For now, just return the URI
                return {"uri": image_url}  # type: ignore

    # No image found
    raise ValueError("No image found in messages")


async def stream_gemini_response(
    messages: List[ChatCompletionMessageParam],
    api_key: str,
    callback: Callable[[str], Awaitable[None]],
    model_name: str,
) -> Completion:
    if genai is None or types is None:
        raise ImportError("Google Generative AI library is not available")
        
    start_time = time.time()

    # Get image data from messages
    image_data = extract_image_from_messages(messages)

    # 根据模型类型设置超时时间
    if model_name == Llm.GEMINI_2_5_FLASH_PREVIEW_05_20.value:
        timeout = GEMINI_PREVIEW_TIMEOUT
    elif model_name in [Llm.GEMINI_2_5_PRO.value, Llm.GEMINI_2_5_FLASH.value]:
        timeout = GEMINI_THINKING_TIMEOUT
    else:
        timeout = GEMINI_DEFAULT_TIMEOUT
    
    client = genai.Client(api_key=api_key)
    full_response = ""

    # Configure model parameters based on model type
    # Using basic configuration to avoid parameter errors
    config = None  # Use default configuration
    
    if model_name == Llm.GEMINI_2_5_FLASH_PREVIEW_05_20.value:
        print(f"Configured {model_name} with preview settings and maximum timeout")
    elif model_name in [Llm.GEMINI_2_5_PRO.value, Llm.GEMINI_2_5_FLASH.value]:
        print(f"Configured {model_name} with thinking support")
    else:
        print(f"Configured {model_name} with standard settings")

    try:
        # 使用asyncio.wait_for实现超时控制
        print(f"Starting Gemini API call for model {model_name} with timeout {timeout}s")
        
        stream = await asyncio.wait_for(
            client.aio.models.generate_content_stream(
                model=model_name,
                contents={
                    "parts": [
                        {"text": messages[0]["content"]},  # type: ignore
                        types.Part.from_bytes(
                            data=base64.b64decode(image_data["data"]),
                            mime_type=image_data["mime_type"],
                        ),
                    ]
                },
                config=config,
            ),
            timeout=timeout
        )
        
        async for chunk in stream:
            if chunk.candidates and len(chunk.candidates) > 0 and chunk.candidates[0].content and chunk.candidates[0].content.parts:
                for part in chunk.candidates[0].content.parts:
                    if not part.text:
                        continue
                    elif part.thought:
                        print("Thought summary:")
                        print(part.text)
                    else:
                        full_response += part.text
                        await callback(part.text)
                        
        print(f"Gemini API call completed successfully in {time.time() - start_time:.2f}s")
        
    except asyncio.TimeoutError:
        print(f"Gemini API call timed out after {timeout}s for model {model_name}")
        raise TimeoutError(f"Gemini API call timed out after {timeout} seconds")
    except Exception as e:
        print(f"Gemini API call failed for model {model_name}: {str(e)}")
        raise

    completion_time = time.time() - start_time
    return {"duration": completion_time, "code": full_response}
