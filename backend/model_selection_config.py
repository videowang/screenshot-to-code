from llm import Llm
from typing import Dict, List

# 四种模式的模型配置
# 根据模型能力、性能和适用场景进行优化排序
MODEL_SELECTION_CONFIG: Dict[str, List[Llm]] = {
    # 文本创建模式 - 优先考虑推理能力和代码生成质量
    "create_text": [
        Llm.GPT_4_1_2025_04_14,           # 最新GPT-4.1，最强推理能力
        Llm.CLAUDE_4_SONNET_2025_05_14,   # Claude 4 Sonnet，优秀的代码生成
        Llm.GEMINI_2_5_PRO,               # Gemini 2.5 Pro，支持thinking，高质量输出
        Llm.CLAUDE_3_7_SONNET_2025_02_19, # Claude 3.7 Sonnet，平衡性能
        Llm.GPT_4O_2024_11_20,            # GPT-4o，多模态能力
        Llm.CLAUDE_3_5_SONNET_2024_10_22, # Claude 3.5 Sonnet，稳定选择
    ],
    # 非文本创建模式 - 优先考虑多模态处理和thinking能力
    "create_non_text": [
        # Llm.GEMINI_2_5_FLASH_PREVIEW_05_20, # Gemini 2.5 Flash的预发布版本
        Llm.GEMINI_2_5_PRO,                 # Pro版本，高质量thinking
        Llm.GEMINI_2_5_FLASH,               # Flash版本，平衡速度和质量
        Llm.GEMINI_2_0_FLASH,               # 2.0版本，稳定多模态
        Llm.GEMINI_2_5_FLASH_LITE,          # Lite版本，快速处理
        # Llm.GPT_4_1_NANO_2025_04_14,      # 备用选项
        # Llm.GPT_4_1_MINI_2025_04_14,      # 备用选项
        # Llm.CLAUDE_3_HAIKU,               # 备用选项
    ],
    # 文本更新模式 - 优先考虑理解和修改能力
    "update_text": [
        Llm.GPT_4_1_2025_04_14,           # 最强理解和修改能力
        Llm.CLAUDE_4_SONNET_2025_05_14,   # 优秀的代码理解
        Llm.GEMINI_2_5_PRO,               # 支持thinking的深度分析
        Llm.CLAUDE_3_7_SONNET_2025_02_19, # 稳定的修改能力
        Llm.GPT_4O_2024_11_20,            # 多模态理解
        Llm.CLAUDE_3_5_SONNET_2024_10_22, # 经典选择
    ],
    # 非文本更新模式 - 优先考虑多模态理解和精确修改
    "update_non_text": [
        Llm.GEMINI_2_5_PRO,               # 最佳多模态理解+thinking
        Llm.GPT_4_1_2025_04_14,           # 强大的理解能力
        Llm.GEMINI_2_5_FLASH,             # 快速多模态处理
        Llm.CLAUDE_3_7_SONNET_2025_02_19, # 稳定的修改能力
        Llm.GPT_4O_2024_11_20,            # 多模态支持
        Llm.CLAUDE_3_5_SONNET_2024_10_22, # 备用选择
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