# Variant System

变体系统同时生成多个版本的代码，为用户提供选择并提高成功率。

## 概述

- **默认变体数量**: 4个 (通过 `NUM_VARIANTS` 配置)
- **模型选择**: 基于四种模式配置循环选择模型
- **生成类型**: 根据输入模式和生成类型选择不同的模型组合
- **前端**: 网格布局，支持键盘快捷键
- **后端**: 模型选择管道，使用WebSocket消息传递

## 模型选择逻辑

系统基于四种模式配置选择模型，每种模式都有优化的模型列表：

### 四种模式配置

1. **create_text**: 文本创建模式 - 优先考虑推理能力和代码生成质量
2. **create_non_text**: 非文本创建模式 - 优先考虑多模态处理和thinking能力
3. **update_text**: 文本更新模式 - 优先考虑理解和修改能力
4. **update_non_text**: 非文本更新模式 - 优先考虑多模态理解和精确修改

### 模式键生成逻辑

```python
if input_mode == "text":
    mode_key = f"{generation_type}_text"
else:
    mode_key = f"{generation_type}_non_text"
```

### 循环选择算法

系统使用循环选择算法为4个变体分配模型：

```python
for i in range(num_variants):
    selected_models.append(models[i % len(models)])
```

### 模型配置获取

实际的模型配置定义在 `backend/model_selection_config.py` 的 `MODEL_SELECTION_CONFIG` 字典中。每种模式包含按优先级排序的模型列表，例如：

- **create_non_text模式** (图片输入默认): Gemini 2.5 Pro, Gemini 2.5 Flash, Gemini 2.0 Flash, Gemini 2.5 Flash Lite
- **create_text模式**: GPT-4.1, Claude 4 Sonnet, Gemini 2.5 Pro 等

具体模型列表会根据性能和能力进行调整，请参考配置文件获取最新信息。

## API密钥管理

### 环境变量配置

系统支持三种AI提供商的API密钥：

```python
OPENAI_API_KEY = os.environ.get("OPENAI_API_KEY", None)
ANTHROPIC_API_KEY = os.environ.get("ANTHROPIC_API_KEY", None)
GEMINI_API_KEY = os.environ.get("GEMINI_API_KEY", None)
```

**配置方式**: 在 `backend/.env` 文件中设置实际的API密钥：

```bash
OPENAI_API_KEY=your_openai_api_key_here
ANTHROPIC_API_KEY=your_anthropic_api_key_here
GEMINI_API_KEY=your_gemini_api_key_here
```

### 密钥检查时机

- **模型选择阶段**: 不检查API密钥，直接选择模型
- **执行阶段**: 在实际调用API时检查密钥
- **错误处理**: 缺少密钥时发送 `variantError` 消息给前端

### 错误处理流程

每个提供商都有专门的错误处理：

- **OpenAI**: 认证错误、模型未找到、配额限制
- **Anthropic**: API密钥缺失、通用错误
- **Gemini**: API密钥缺失、通用错误

使用 `VariantErrorAlreadySent` 异常避免重复错误消息。

## 前端界面

### 网格布局
- **2 variants**: 2-column 
- **3 variants**: 2-column (third wraps below - prevents squishing)
- **4 variants**: 2x2 grid  
- **5-6 variants**: 3-column 
- **7+ variants**: 4-column

### 键盘快捷键
- **Option/Alt + 1, 2, 3, 4**: 切换变体
- 全局生效，即使在文本字段中也可使用
- 使用 `event.code` 确保跨平台兼容性
- 视觉指示器显示 ⌥1, ⌥2, ⌥3, ⌥4

## 架构

### 后端
- `StatusBroadcastMiddleware` 向前端发送 `variantCount`
- `ModelSelectionStage` 循环选择可用模型
- 管道通过WebSocket并行生成变体

### 前端  
- 从后端动态学习变体数量
- `resizeVariants()` 根据后端数量调整UI
- 每个变体独立错误处理和状态显示

## WebSocket消息

```typescript
"variantCount" | "chunk" | "status" | "setCode" | "variantComplete" | "variantError"
```

## 实现特性

### 可扩展性
- 通过更新 `MODEL_SELECTION_CONFIG` 轻松添加新模型
- 通过 `NUM_VARIANTS` 环境变量配置变体数量
- 独立的变体处理防止级联故障

### 跨平台兼容
- 支持任意API密钥组合
- 模型不可用时优雅降级
- 无论激活哪些模型都保持一致的接口

### 特殊模式
- **视频模式**: 使用固定的Claude 3 Opus模型
- **Mock模式**: 当 `SHOULD_MOCK_AI_RESPONSE=true` 时使用模拟响应

## 关键文件

- `backend/model_selection_config.py`: 模型配置和选择逻辑
- `backend/routes/generate_code.py`: 主要生成管道
- `backend/config.py`: 配置和API密钥
- `backend/.env`: API密钥环境变量配置文件
- `backend/llm.py`: 模型枚举和提供商映射
- `frontend/src/components/variants/Variants.tsx`: UI和快捷键
- `frontend/src/store/project-store.ts`: 状态管理

## 配置更新

要修改模型配置，请编辑 `backend/model_selection_config.py` 中的 `MODEL_SELECTION_CONFIG` 字典。每种模式的模型按优先级排序，系统会根据变体数量循环选择。
