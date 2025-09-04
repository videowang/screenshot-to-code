from llm import Llm
from typing import Dict, List

# 四种模式的模型配置
MODEL_SELECTION_CONFIG: Dict[str, List[Llm]] = {
    "create_text": [
        Llm.GPT_4_1_2025_04_14,
        Llm.CLAUDE_3_7_SONNET_2025_02_19,
        Llm.CLAUDE_4_SONNET_2025_05_14,
        Llm.GPT_4O_2024_11_20,
        Llm.CLAUDE_3_5_SONNET_2024_10_22,
    ],
    "create_non_text": [
        Llm.GPT_4_1_NANO_2025_04_14,
        Llm.GPT_4_1_MINI_2025_04_14,
        Llm.GEMINI_2_0_FLASH,
        Llm.CLAUDE_3_HAIKU,
        Llm.GEMINI_2_5_FLASH_PREVIEW_05_20,
    ],
    "update_text": [
        Llm.GPT_4_1_2025_04_14,
        Llm.CLAUDE_3_7_SONNET_2025_02_19,
        Llm.CLAUDE_4_SONNET_2025_05_14,
        Llm.GPT_4O_2024_11_20,
        Llm.CLAUDE_3_5_SONNET_2024_10_22,
    ],
    "update_non_text": [
        Llm.GPT_4_1_2025_04_14,
        Llm.CLAUDE_3_7_SONNET_2025_02_19,
        Llm.CLAUDE_3_7_SONNET_2025_02_19,  # Gemini不支持更新，使用Claude替代
        Llm.GPT_4O_2024_11_20,
        Llm.CLAUDE_3_5_SONNET_2024_10_22,
    ],
}


def get_variant_models(generation_type: str, input_mode: str, num_variants: int) -> List[Llm]:
    """根据配置获取变体模型列表"""
    # 确定模式键
    if input_mode == "text":
        mode_key = f"{generation_type}_text"
    else:
        mode_key = f"{generation_type}_non_text"
    
    # 获取配置的模型列表
    models = MODEL_SELECTION_CONFIG.get(mode_key, [])
    if not models:
        raise ValueError(f"未找到模式 {mode_key} 的模型配置")
    
    # 循环选择模型
    selected_models: List[Llm] = []
    for i in range(num_variants):
        selected_models.append(models[i % len(models)])
    
    return selected_models