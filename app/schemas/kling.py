from enum import Enum
from typing import Optional, List, Union, Dict, Any
from pydantic import BaseModel, Field, field_validator, model_validator

# --- Enums ---

class ModelName(str, Enum):
    V1 = "kling-v1"
    V1_5 = "kling-v1-5"
    V1_6 = "kling-v1-6"
    V2 = "kling-v2"
    V2_MASTER = "kling-v2-master"
    O1 = "kling-image-o1"

class Mode(str, Enum):
    STD = "std"
    PRO = "pro"

class AspectRatio(str, Enum):
    R_16_9 = "16:9"
    R_9_16 = "9:16"
    R_1_1 = "1:1"
    R_4_3 = "4:3"
    R_3_4 = "3:4"
    R_3_2 = "3:2"
    R_2_3 = "2:3"
    R_21_9 = "21:9"
    AUTO = "auto"

class CameraControlType(str, Enum):
    SIMPLE = "simple"
    DOWN_BACK = "down_back"
    FORWARD_UP = "forward_up"
    RIGHT_TURN_FORWARD = "right_turn_forward"
    LEFT_TURN_FORWARD = "left_turn_forward"

class TaskStatus(str, Enum):
    SUBMITTED = "submitted"
    PROCESSING = "processing"
    SUCCEED = "succeed"
    FAILED = "failed"

# --- Common Validators ---

def clean_base64_field(v: Optional[str]) -> Optional[str]:
    if v and isinstance(v, str) and v.startswith('data:'):
        # Find the comma separator
        parts = v.split(',', 1)
        if len(parts) == 2:
            return parts[1]
    return v

# --- Complex Objects ---

class CameraControlConfig(BaseModel):
    horizontal: float = Field(0, ge=-10, le=10)
    vertical: float = Field(0, ge=-10, le=10)
    pan: float = Field(0, ge=-10, le=10)
    tilt: float = Field(0, ge=-10, le=10)
    roll: float = Field(0, ge=-10, le=10)
    zoom: float = Field(0, ge=-10, le=10)

    @model_validator(mode='after')
    def check_at_least_one_nonzero(self):
        # Check if all fields are 0
        if all(getattr(self, field) == 0 for field in self.model_fields):
            raise ValueError("camera_control.config must have at least one non-zero field")
        return self

class CameraControl(BaseModel):
    type: CameraControlType
    config: Optional[CameraControlConfig] = None

    @model_validator(mode='after')
    def check_config_required(self):
        if self.type == CameraControlType.SIMPLE and not self.config:
            raise ValueError("config is required when type is simple")
        return self

# --- Request Models: Video Generation ---

class Text2VideoRequest(BaseModel):
    model_name: Optional[str] = "kling-v1"
    prompt: str = Field(..., max_length=2500)
    negative_prompt: Optional[str] = Field(None, max_length=2500)
    sound: Optional[str] = "off"
    cfg_scale: Optional[float] = 0.5
    mode: Optional[Mode] = Mode.STD
    aspect_ratio: Optional[AspectRatio] = AspectRatio.R_16_9
    duration: Optional[str] = "5"
    camera_control: Optional[CameraControl] = None
    external_task_id: Optional[str] = None
    callback_url: Optional[str] = None

class Image2VideoRequest(BaseModel):
    model_name: Optional[str] = "kling-v1"
    image: str
    image_tail: Optional[str] = None
    prompt: Optional[str] = None
    negative_prompt: Optional[str] = None
    cfg_scale: Optional[float] = 0.5
    mode: Optional[Mode] = Mode.STD
    duration: Optional[str] = "5"
    aspect_ratio: Optional[AspectRatio] = AspectRatio.R_16_9
    camera_control: Optional[CameraControl] = None
    external_task_id: Optional[str] = None
    callback_url: Optional[str] = None

    @field_validator('image', 'image_tail')
    def validate_base64(cls, v):
        return clean_base64_field(v)

class MultiImage2VideoRequest(BaseModel):
    model_name: Optional[str] = "kling-v1-6"
    image_list: List[str] = Field(..., min_length=1, max_length=4)
    prompt: str
    negative_prompt: Optional[str] = None
    mode: Optional[Mode] = Mode.STD
    duration: Optional[str] = "5"
    aspect_ratio: Optional[AspectRatio] = AspectRatio.R_16_9
    external_task_id: Optional[str] = None
    callback_url: Optional[str] = None

    @field_validator('image_list')
    def validate_image_list(cls, v):
        return [clean_base64_field(img) for img in v]

class MotionControlRequest(BaseModel):
    image_url: str
    video_url: str
    character_orientation: str # 'image' or 'video'
    mode: Mode = Mode.STD
    prompt: Optional[str] = None
    keep_original_sound: Optional[str] = "yes"
    external_task_id: Optional[str] = None
    callback_url: Optional[str] = None

    @field_validator('image_url')
    def validate_image(cls, v):
        return clean_base64_field(v)

class VideoExtendRequest(BaseModel):
    video_id: str
    prompt: Optional[str] = None
    negative_prompt: Optional[str] = None
    cfg_scale: Optional[float] = 0.5
    callback_url: Optional[str] = None

# --- Request Models: Lip Sync ---

class IdentifyFaceRequest(BaseModel):
    video_id: Optional[str] = None
    video_url: Optional[str] = None

    @model_validator(mode='after')
    def check_video_source(self):
        if not self.video_id and not self.video_url:
            raise ValueError("Either video_id or video_url must be provided")
        if self.video_id and self.video_url:
            raise ValueError("Cannot provide both video_id and video_url")
        return self

class FaceChoose(BaseModel):
    face_id: str
    audio_id: Optional[str] = None
    sound_file: Optional[str] = None
    sound_start_time: int
    sound_end_time: int
    sound_insert_time: int
    sound_volume: float = 1.0
    original_audio_volume: float = 1.0

    @field_validator('sound_file')
    def validate_sound_file(cls, v):
        return clean_base64_field(v)

class CreateSyncTaskRequest(BaseModel):
    session_id: str
    face_choose: List[FaceChoose]
    external_task_id: Optional[str] = None
    callback_url: Optional[str] = None

# --- Request Models: Image Generation ---

class GenerateImageRequest(BaseModel):
    model_name: Optional[str] = "kling-v1"
    prompt: str
    negative_prompt: Optional[str] = None
    image: Optional[str] = None
    image_reference: Optional[str] = None # subject, face
    image_fidelity: Optional[float] = 0.5
    human_fidelity: Optional[float] = 0.45
    resolution: Optional[str] = "1k"
    aspect_ratio: Optional[AspectRatio] = AspectRatio.R_16_9
    n: Optional[int] = 1
    callback_url: Optional[str] = None

    @field_validator('image')
    def validate_image(cls, v):
        return clean_base64_field(v)

class OmniImageRequest(BaseModel):
    model_name: Optional[str] = "kling-image-o1"
    prompt: str
    image_list: Optional[List[str]] = None
    element_list: Optional[List[Any]] = None # Not fully detailed in spec, leaving as Any or List[dict]
    resolution: Optional[str] = "1k"
    aspect_ratio: Optional[AspectRatio] = AspectRatio.AUTO
    n: Optional[int] = 1
    external_task_id: Optional[str] = None
    callback_url: Optional[str] = None

    @field_validator('image_list')
    def validate_image_list(cls, v):
        if v:
            return [clean_base64_field(img) for img in v]
        return v

# --- Response Models ---

class TaskResponse(BaseModel):
    task_id: str
    message: str = "success"
    raw_data: Dict[str, Any] # Contains original 'data' field from Kling API
