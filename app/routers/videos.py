import httpx
from fastapi import APIRouter, Depends, HTTPException
from app.schemas.kling import (
    Text2VideoRequest, Image2VideoRequest, MultiImage2VideoRequest, 
    MotionControlRequest, VideoExtendRequest, TaskResponse
)
from app.services.kling_client import KlingClient, get_kling_client
import logging

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/api/v1/videos", tags=["Video Generation"])

@router.post("/text2video", response_model=TaskResponse)
async def create_text2video(request: Text2VideoRequest, client: KlingClient = Depends(get_kling_client)):
    try:
        data = request.model_dump(mode='json', exclude_none=True)
        # Log the outgoing payload for debugging
        logger.info(f"Sending payload to Kling: {data}")
        
        response = await client.create_text2video(data)
        
        # Log response for debugging
        logger.info(f"Received response from Kling: {response}")

        if response.get("code") != 0:
            raise HTTPException(status_code=400, detail=response.get("message", "Unknown error"))
        task_data = response.get("data", {})
        return TaskResponse(
            task_id=task_data.get("task_id", ""),
            raw_data=task_data
        )
    except HTTPException:
        raise
    except httpx.HTTPStatusError as e:
        detail = e.response.text
        try:
            detail_json = e.response.json()
            detail = detail_json.get("message", detail)
            # Log the error detail
            logger.error(f"Kling API Error (HTTP {e.response.status_code}): {detail}")
        except Exception:
            logger.error(f"Kling API Error (HTTP {e.response.status_code}): {detail}")
        raise HTTPException(status_code=e.response.status_code, detail=detail)
    except Exception as e:
        logger.error(f"Unexpected error: {str(e)}")
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
    except httpx.HTTPStatusError as e:
        detail = e.response.text
        try:
            detail_json = e.response.json()
            detail = detail_json.get("message", detail)
        except Exception:
            pass
        raise HTTPException(status_code=e.response.status_code, detail=detail)
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
    except httpx.HTTPStatusError as e:
        detail = e.response.text
        try:
            detail_json = e.response.json()
            detail = detail_json.get("message", detail)
        except Exception:
            pass
        raise HTTPException(status_code=e.response.status_code, detail=detail)
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
    except httpx.HTTPStatusError as e:
        detail = e.response.text
        try:
            detail_json = e.response.json()
            detail = detail_json.get("message", detail)
        except Exception:
            pass
        raise HTTPException(status_code=e.response.status_code, detail=detail)
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
    except httpx.HTTPStatusError as e:
        detail = e.response.text
        try:
            detail_json = e.response.json()
            detail = detail_json.get("message", detail)
        except Exception:
            pass
        raise HTTPException(status_code=e.response.status_code, detail=detail)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
