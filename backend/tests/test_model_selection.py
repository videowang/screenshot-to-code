import pytest
from unittest.mock import AsyncMock
from routes.generate_code import ModelSelectionStage
from llm import Llm


class TestModelSelectionAllKeys:
    """Test model selection when all API keys are present."""

    def setup_method(self):
        """Set up test fixtures."""
        mock_throw_error = AsyncMock()
        self.model_selector = ModelSelectionStage(mock_throw_error)

    @pytest.mark.asyncio
    async def test_text_create(self):
        """Text + Create: 根据配置循环选择模型"""
        models = await self.model_selector.select_models(
            generation_type="create",
            input_mode="text",
        )
        
        expected = [
            Llm.GPT_4_1_2025_04_14,
            Llm.CLAUDE_3_7_SONNET_2025_02_19,
            Llm.CLAUDE_4_SONNET_2025_05_14,
            Llm.GPT_4O_2024_11_20,  # NUM_VARIANTS=4, 按配置循环
        ]
        assert models == expected

    @pytest.mark.asyncio
    async def test_text_update(self):
        """Text + Update: 根据配置循环选择模型"""
        models = await self.model_selector.select_models(
            generation_type="update",
            input_mode="text",
        )
        
        expected = [
            Llm.GPT_4_1_2025_04_14,
            Llm.CLAUDE_3_7_SONNET_2025_02_19,
            Llm.CLAUDE_4_SONNET_2025_05_14,
            Llm.GPT_4O_2024_11_20,  # NUM_VARIANTS=4, 按配置循环
        ]
        assert models == expected

    @pytest.mark.asyncio
    async def test_image_create(self):
        """Image + Create: 根据配置循环选择模型"""
        models = await self.model_selector.select_models(
            generation_type="create",
            input_mode="image",
        )
        
        expected = [
            Llm.GPT_4_1_NANO_2025_04_14,
            Llm.GPT_4_1_MINI_2025_04_14,
            Llm.GEMINI_2_0_FLASH,
            Llm.CLAUDE_3_HAIKU,  # NUM_VARIANTS=4, 按配置循环
        ]
        assert models == expected

    @pytest.mark.asyncio
    async def test_image_update(self):
        """Image + Update: 根据配置循环选择模型（Gemini不支持更新已在配置中处理）"""
        models = await self.model_selector.select_models(
            generation_type="update",
            input_mode="image",
        )
        
        expected = [
            Llm.GPT_4_1_2025_04_14,
            Llm.CLAUDE_3_7_SONNET_2025_02_19,
            Llm.CLAUDE_3_7_SONNET_2025_02_19,  # 配置中已处理Gemini不支持更新的情况
            Llm.GPT_4O_2024_11_20,  # NUM_VARIANTS=4, 按配置循环
        ]
        assert models == expected
