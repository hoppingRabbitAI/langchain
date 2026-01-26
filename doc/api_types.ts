// api_types.ts
// Generated based on Pydantic models in app/schemas/kling.py

// --- Enums ---

export enum ModelName {
  V1 = "kling-v1",
  V1_5 = "kling-v1-5",
  V1_6 = "kling-v1-6",
  V2 = "kling-v2",
  V2_MASTER = "kling-v2-master",
  O1 = "kling-image-o1"
}

export enum Mode {
  STD = "std",
  PRO = "pro"
}

export enum AspectRatio {
  R_16_9 = "16:9",
  R_9_16 = "9:16",
  R_1_1 = "1:1",
  R_4_3 = "4:3",
  R_3_4 = "3:4",
  R_3_2 = "3:2",
  R_2_3 = "2:3",
  R_21_9 = "21:9",
  AUTO = "auto"
}

export enum CameraControlType {
  SIMPLE = "simple",
  DOWN_BACK = "down_back",
  FORWARD_UP = "forward_up",
  RIGHT_TURN_FORWARD = "right_turn_forward",
  LEFT_TURN_FORWARD = "left_turn_forward"
}

export enum TaskStatus {
  SUBMITTED = "submitted",
  PROCESSING = "processing",
  SUCCEED = "succeed",
  FAILED = "failed"
}

// --- Common Objects ---

export interface CameraControlConfig {
  horizontal?: number; // range [-10, 10]
  vertical?: number;
  pan?: number;
  tilt?: number;
  roll?: number;
  zoom?: number;
}

export interface CameraControl {
  type: CameraControlType;
  config?: CameraControlConfig;
}

export interface FaceChoose {
  face_id: string;
  audio_id?: string;
  sound_file?: string; // Base64 or URL
  sound_start_time: number;
  sound_end_time: number;
  sound_insert_time: number;
  sound_volume?: number;
  original_audio_volume?: number;
}

// --- Request Interfaces ---

export interface Text2VideoRequest {
  model_name?: string; // Default "kling-v1"
  prompt: string; // Max 2500 chars
  negative_prompt?: string;
  sound?: string; // "on" | "off"
  cfg_scale?: number; // 0.0 - 1.0
  mode?: Mode;
  aspect_ratio?: AspectRatio;
  duration?: string; // "5" | "10"
  camera_control?: CameraControl;
  external_task_id?: string;
  callback_url?: string;
}

export interface Image2VideoRequest {
  model_name?: string; // Default "kling-v1"
  image: string; // Base64 or URL
  image_tail?: string;
  prompt?: string;
  negative_prompt?: string;
  cfg_scale?: number;
  mode?: Mode;
  duration?: string;
  aspect_ratio?: AspectRatio;
  camera_control?: CameraControl;
  external_task_id?: string;
  callback_url?: string;
}

export interface MultiImage2VideoRequest {
  model_name?: string; // Default "kling-v1-6"
  image_list: string[]; // 1-4 images
  prompt: string;
  negative_prompt?: string;
  mode?: Mode;
  duration?: string;
  aspect_ratio?: AspectRatio;
  external_task_id?: string;
  callback_url?: string;
}

export interface MotionControlRequest {
  image_url: string;
  video_url: string;
  character_orientation: string; // 'image' | 'video'
  mode?: Mode;
  prompt?: string;
  keep_original_sound?: string; // "yes" | "no"
  external_task_id?: string;
  callback_url?: string;
}

export interface VideoExtendRequest {
  video_id: string;
  prompt?: string;
  negative_prompt?: string;
  cfg_scale?: number;
  callback_url?: string;
}

export interface IdentifyFaceRequest {
  video_id?: string;
  video_url?: string;
}

export interface CreateSyncTaskRequest {
  session_id: string;
  face_choose: FaceChoose[];
  external_task_id?: string;
  callback_url?: string;
}

export interface GenerateImageRequest {
  model_name?: string;
  prompt: string;
  negative_prompt?: string;
  image?: string;
  image_reference?: string; // 'subject' | 'face'
  image_fidelity?: number;
  human_fidelity?: number;
  resolution?: string; // "1k" | "2k"
  aspect_ratio?: AspectRatio;
  n?: number;
  callback_url?: string;
}

export interface OmniImageRequest {
  model_name?: string;
  prompt: string;
  image_list?: string[];
  element_list?: any[]; // Complex structure not fully typed
  resolution?: string;
  aspect_ratio?: AspectRatio;
  n?: number;
  external_task_id?: string;
  callback_url?: string;
}

// --- Response Interfaces ---

export interface TaskResponse {
  task_id: string;
  message: string;
  raw_data: {
    code?: number;
    message?: string;
    request_id?: string;
    data?: any; // Original Kling data payload
    [key: string]: any;
  };
}

// --- Helper Type for API Error ---
export interface ApiError {
  detail: string | any;
}
