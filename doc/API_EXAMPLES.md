# API 请求示例与参数说明 (API Examples)

本文档提供了所有 Kling AI 集成接口的标准 JSON 请求体和预期响应。请参考这些示例进行调试。

---

## 1. 视频生成 (Video Generation)

### 1.1 文生视频 (Text to Video)

**Endpoint**: `POST /api/v1/videos/text2video`

**请求体 (Minimal)**:
```json
{
  "prompt": "A cinematic shot of a cyberpunk city, night time, rain, neon lights, highly detailed, 4k",
  "model_name": "kling-v1",
  "aspect_ratio": "16:9",
  "duration": "5"
}
```

**请求体 (Full)**:
```json
{
  "model_name": "kling-v1",
  "prompt": "A golden retriever running on the beach",
  "negative_prompt": "blur, low quality, distortion",
  "cfg_scale": 0.5,
  "mode": "std",
  "aspect_ratio": "16:9",
  "duration": "5",
  "camera_control": {
    "type": "simple",
    "config": {
      "zoom": 0.5,
      "pan": 0.0,
      "tilt": 0.0,
      "roll": 0.0,
      "horizontal": 0.0,
      "vertical": 0.0
    }
  },
  "callback_url": "https://your-domain.com/callback"
}
```

**响应体**:
```json
{
  "task_id": "845014248110960707",
  "message": "success",
  "raw_data": { ... }
}
```

### 1.2 图生视频 (Image to Video)

**Endpoint**: `POST /api/v1/videos/image2video`

**请求体**:
```json
{
  "model_name": "kling-v1",
  "image": "https://example.com/start_frame.jpg",
  "image_tail": "https://example.com/end_frame.jpg",
  "prompt": "The car drives forward",
  "cfg_scale": 0.5,
  "mode": "std",
  "duration": "5"
}
```
*注意：`image` 也可以是 Base64 字符串（无需前缀）。*

---

## 2. 图像生成 (Image Generation)

### 2.1 标准生图 (Text to Image)

**Endpoint**: `POST /api/v1/images/generations`

**请求体**:
```json
{
  "model_name": "kling-v1",
  "prompt": "A cute cat sitting on a sofa",
  "n": 1,
  "aspect_ratio": "1:1"
}
```

### 2.2 图生图 (Image to Image)

**Endpoint**: `POST /api/v1/images/generations`

**请求体**:
```json
{
  "model_name": "kling-v1-5",
  "prompt": "Make it look like a painting",
  "image": "https://example.com/source.jpg",
  "image_fidelity": 0.6
}
```

### 2.3 Omni-Image (高级生图)

**Endpoint**: `POST /api/v1/images/omni-image`

**请求体**:
```json
{
  "model_name": "kling-image-o1",
  "prompt": "A futuristic warrior holding <<<image_1>>>",
  "image_list": [
    "https://example.com/sword.jpg"
  ],
  "aspect_ratio": "auto"
}
```

---

## 3. 口型同步 (Lip Sync)

### 3.1 人脸识别 (Identify Face)

**Endpoint**: `POST /api/v1/lipsync/identify-face`

**请求体**:
```json
{
  "video_url": "https://example.com/video_with_face.mp4"
}
```

**响应体**:
```json
{
  "session_id": "sess_123...",
  "face_data": [
    {
      "face_id": "face_abc...",
      "start_time": 0,
      "end_time": 5000
    }
  ]
}
```

### 3.2 创建对口型任务 (Create Task)

**Endpoint**: `POST /api/v1/lipsync/create-task`

**请求体**:
```json
{
  "session_id": "sess_123...",
  "face_choose": [
    {
      "face_id": "face_abc...",
      "sound_file": "https://example.com/audio.mp3",
      "sound_start_time": 0,
      "sound_end_time": 5000,
      "sound_insert_time": 0
    }
  ]
}
```

---

## 4. 任务查询 (Query Task)

**Endpoint**: `GET /api/v1/tasks/{category}/{task_type}/{task_id}`

**示例**:
- 查视频任务: `GET /api/v1/tasks/videos/text2video/845014248110960707`
- 查生图任务: `GET /api/v1/tasks/images/generations/task_img_123`

**响应 (成功)**:
```json
{
  "task_id": "845014248110960707",
  "message": "succeed",
  "raw_data": {
    "task_result": {
      "videos": [
        { "url": "https://cdn.klingai.com/..." }
      ]
    }
  }
}
```
