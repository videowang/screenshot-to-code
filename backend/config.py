# Useful for debugging purposes when you don't want to waste GPT4-Vision credits
# Setting to True will stream a mock response instead of calling the OpenAI API
# TODO: Should only be set to true when value is 'True', not any abitrary truthy value
import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

NUM_VARIANTS = 4

# LLM-related
OPENAI_API_KEY = os.environ.get("OPENAI_API_KEY", None)
ANTHROPIC_API_KEY = os.environ.get("ANTHROPIC_API_KEY", None)
GEMINI_API_KEY = os.environ.get("GEMINI_API_KEY", None)
OPENAI_BASE_URL = os.environ.get("OPENAI_BASE_URL", None)

# Image generation (optional)
REPLICATE_API_KEY = os.environ.get("REPLICATE_API_KEY", None)

# Debugging-related

SHOULD_MOCK_AI_RESPONSE = os.environ.get("MOCK", "false").lower() == "true"
IS_DEBUG_ENABLED = bool(os.environ.get("IS_DEBUG_ENABLED", False))
DEBUG_DIR = os.environ.get("DEBUG_DIR", "")

# Set to True when running in production (on the hosted version)
# Used as a feature flag to enable or disable certain features
IS_PROD = os.environ.get("IS_PROD", False)

# API Timeout configurations (in seconds)
GEMINI_DEFAULT_TIMEOUT = int(os.environ.get("GEMINI_DEFAULT_TIMEOUT", "300"))  # 5 minutes
GEMINI_THINKING_TIMEOUT = int(os.environ.get("GEMINI_THINKING_TIMEOUT", "900"))  # 15 minutes
GEMINI_PREVIEW_TIMEOUT = int(os.environ.get("GEMINI_PREVIEW_TIMEOUT", "1200"))  # 20 minutes
OPENAI_TIMEOUT = int(os.environ.get("OPENAI_TIMEOUT", "600"))  # 10 minutes
ANTHROPIC_TIMEOUT = int(os.environ.get("ANTHROPIC_TIMEOUT", "600"))  # 10 minutes
