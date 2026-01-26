# Kling AI API Integration Specification (FastAPI)

## 1. 项目技术栈要求

- **Framework**: FastAPI (Async)
- **Validation**: Pydantic v2
- **Client**: HTTPX (AsyncClient)
- **Structure**: 采用 `Router` -> `Service` -> `Client` 的分层架构。
- **Auth**: Bearer Token (在 Header 中设置 `Authorization`)

## 2. 全局配置

- **Base URL**: `https://api.klingai.com/v1` (或 `https://api-beijing.klingai.com/v1`，视环境而定)
- **Common Headers**:
  - `Content-Type`: `application/json`
  - `Authorization`: `Bearer {YOUR_JWT_TOKEN}`

## 3. 核心业务模块与路由定义

请为以下每个模块生成独立的 `APIRouter` 和对应的 Pydantic Request/Response 模型。

### 模块 A: 视频生成 (Video Generation)

**Router Prefix**: `/api/v1/videos`

| **功能点**     | **内部方法名**       | **Kling API 路径 (POST)**   | **关键参数备注**                                            |
| -------------- | -------------------- | --------------------------- | ----------------------------------------------------------- |
| **文生视频**   | `create_text2video`  | `/videos/text2video`        | `prompt` (必填), `camera_control` (复杂对象)                |
| **图生视频**   | `create_image2video` | `/videos/image2video`       | `image` (必填), `image_tail`, 动态/静态Mask互斥             |
| **多图生视频** | `create_multi_image` | `/videos/multi-image2video` | `image_list` (1-4张), 模型仅 `kling-v1-6`                   |
| **动作控制**   | `create_motion_ctrl` | `/videos/motion-control`    | `image_url` + `video_url` (均必填), `character_orientation` |
| **视频延长**   | `extend_video`       | `/videos/video-extend`      | `video_id` (必填), 仅支持生成30天内的视频                   |

### 模块 B: 口型同步 (Lip Sync)

**Router Prefix**: `/api/v1/lipsync`

| **功能点**     | **内部方法名**     | **Kling API 路径 (POST)**   | **关键参数备注**                              |
| -------------- | ------------------ | --------------------------- | --------------------------------------------- |
| **人脸识别**   | `identify_face`    | `/videos/identify-face`     | `video_id` 或 `video_url` (二选一)            |
| **创建对口型** | `create_sync_task` | `/videos/advanced-lip-sync` | 需 `session_id` (来自识别接口), `face_choose` |

### 模块 C: 图像生成 (Image Generation)

**Router Prefix**: `/api/v1/images`

| **功能点**     | **内部方法名**   | **Kling API 路径 (POST)** | **关键参数备注**                              |
| -------------- | ---------------- | ------------------------- | --------------------------------------------- |
| **标准生图**   | `generate_image` | `/images/generations`     | 支持文生图 & 图生图 (`image` 字段)            |
| **Omni-Image** | `generate_omni`  | `/images/omni-image`      | Prompt支持 `<<<image_1>>>` 语法, `image_list` |

### 模块 D: 任务查询 (Task Query)

**Router Prefix**: `/api/v1/tasks`

- **统一查询接口**: 建议封装一个通用查询，或按模块分发。
- **Kling API 路径**: `GET /{type}/{task_id}` (e.g., `/videos/text2video/{id}`)
- **Response**: 包含 `task_status` (submitted, processing, succeed, failed) 和 `task_result` (url, duration)。

------

## 4. Pydantic 模型核心约束 (Data Models)

请在生成代码时严格遵守以下字段类型和校验规则：

### 4.1 通用枚举 (Enums)

Python

```
class ModelName(str, Enum):
    V1 = "kling-v1"
    V1_5 = "kling-v1-5" # 仅图生图/生图
    V1_6 = "kling-v1-6"
    V2 = "kling-v2"
    V2_MASTER = "kling-v2-master"
    O1 = "kling-image-o1" # 仅Omni

class Mode(str, Enum):
    STD = "std" # 标准
    PRO = "pro" # 专家

class AspectRatio(str, Enum):
    R_16_9 = "16:9"
    R_9_16 = "9:16"
    R_1_1 = "1:1"
    # Omni还支持 auto, 4:3 等

class CameraControlType(str, Enum):
    SIMPLE = "simple"
    DOWN_BACK = "down_back"
    FORWARD_UP = "forward_up"
    RIGHT_TURN_FORWARD = "right_turn_forward"
    LEFT_TURN_FORWARD = "left_turn_forward"
```

### 4.2 关键校验逻辑 (Validators)

1. **Base64 格式清洗**:
   - 所有涉及图片/音频上传的 Base64 字段（如 `image`, `sound_file`），**必须**移除 `data:image/xxx;base64,` 前缀。
   - *Action*: 在 Pydantic 中使用 `@field_validator` 自动清洗。
2. **互斥参数检查**:
   - **LipSync**: `video_id` 和 `video_url` 不能同时存在，也不能同时为空。
   - **Text2Video**: `camera_control.config` 仅在 `type="simple"` 时允许存在。
   - **Image2Video**: `image` + `image_tail` 与 `dynamic_masks` 互斥。

### 4.3 复杂对象结构

**CameraControl Config**:

JSON

```
{
  "type": "simple",
  "config": {
    "horizontal": 0, // range [-10, 10]
    "vertical": 0,
    "pan": 0,
    "tilt": 0,
    "roll": 0,
    "zoom": 0
    // 6选1，其余必须为0
  }
}
```

**Omni-Image Prompt Logic**:

- 如果 `image_list` 有值，`prompt` 中应包含 `<<<image_1>>>` 等占位符。

------

## 5. 错误处理与响应标准化

- **Error Handling**: 捕获 HTTP 异常，统一返回 500 或 400。

- **Standard Response**:

  所有接口应返回统一结构，例如：

  Python

  ```
  class TaskResponse(BaseModel):
      task_id: str
      message: str = "success"
      raw_data: dict # 包含Kling原始返回的 data 字段
  ```

------

## 6. 开发指令 (Prompt for AI)

> **请扮演一名资深 Python 后端工程师，基于上述 API 规范，使用 FastAPI 构建一个视频剪辑网站的后端集成模块。请分步完成以下代码：**
>
> 1. **`app/schemas/kling.py`**: 定义所有 Request Body 的 Pydantic 模型，包含 Base64 清洗 validator 和 Enum 定义。
> 2. **`app/services/kling_client.py`**: 封装 HTTPX 客户端，包含 Authentication Header 的注入和 POST/GET 通用方法。
> 3. **`app/routers`**: 为 "文生视频"、"图生视频"、"口型同步"、"Omni生图" 创建路由文件。
> 4. **`main.py`**: 展示如何注册这些 Router。
>
> **特别注意**:
>
> - 确保 `image` 字段的 Base64 校验逻辑正确。
> - 确保 `model_name` 在不同接口使用正确的默认值。
> - 代码需要包含详细的类型注解 (Type Hints)。