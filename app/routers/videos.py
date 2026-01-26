from fastapi import APIRouter, Depends, HTTPException
from app.schemas.kling import (
    Text2VideoRequest, Image2VideoRequest, MultiImage2VideoRequest, 
    MotionControlRequest, VideoExtendRequest, TaskResponse
)
from app.services.kling_client import KlingClient, get_kling_client

router = APIRouter(prefix="/api/v1/videos", tags=["Video Generation"])

@router.post("/text2video", response_model=TaskResponse)
async def create_text2video(request: Text2VideoRequest, client: KlingClient = Depends(get_kling_client)):
    try:
        data = request.model_dump(exclude_none=True)
        # Handle enum serialization if needed (Pydantic v2 usually handles this well with mode='json')
        # But here we are dumping to dict for requests. Enums will be members.
        # We need values. model_dump(mode='json') creates dict with strings.
        data = request.model_dump(mode='json', exclude_none=True)
        
        response = await client.create_text2video(data)
        
        # Check for API logic error (code != 0)
        if response.get("code") != 0:
            raise HTTPException(status_code=400, detail=response.get("message", "Unknown error"))
            
        task_data = response.get("data", {})
        return TaskResponse(
            task_id=task_data.get("task_id", ""),
            raw_data=task_data
        )
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/image2video", response_model=TaskResponse)
async def create_image2video(request: Image2VideoRequest, client: KlingClient = Depends(get_kling_client)):
    try:
        data = request.model_dump(mode='json', exclude_none=True)
        response = await client.create_image2video(data)
        if response.get("code") != 0:
            raise HTTPException(status_code=400, detail=response.get("message", "Unknown error"))
        task_data = response.get("data", {})
        return TaskResponse(
            task_id=task_data.get("task_id", ""),
            raw_data=task_data
        )
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/multi-image2video", response_model=TaskResponse)
async def create_multi_image(request: MultiImage2VideoRequest, client: KlingClient = Depends(get_kling_client)):
    try:
        data = request.model_dump(mode='json', exclude_none=True)
        response = await client.create_multi_image2video(data)
        if response.get("code") != 0:
            raise HTTPException(status_code=400, detail=response.get("message", "Unknown error"))
        task_data = response.get("data", {})
        return TaskResponse(
            task_id=task_data.get("task_id", ""),
            raw_data=task_data
        )
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/motion-control", response_model=TaskResponse)
async def create_motion_ctrl(request: MotionControlRequest, client: KlingClient = Depends(get_kling_client)):
    try:
        data = request.model_dump(mode='json', exclude_none=True)
        response = await client.create_motion_control(data)
        if response.get("code") != 0:
            raise HTTPException(status_code=400, detail=response.get("message", "Unknown error"))
        task_data = response.get("data", {})
        return TaskResponse(
            task_id=task_data.get("task_id", ""),
            raw_data=task_data
        )
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/video-extend", response_model=TaskResponse)
async def extend_video(request: VideoExtendRequest, client: KlingClient = Depends(get_kling_client)):
    try:
        data = request.model_dump(mode='json', exclude_none=True)
        response = await client.extend_video(data)
        if response.get("code") != 0:
            raise HTTPException(status_code=400, detail=response.get("message", "Unknown error"))
        task_data = response.get("data", {})
        return TaskResponse(
            task_id=task_data.get("task_id", ""),
            raw_data=task_data
        )
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
