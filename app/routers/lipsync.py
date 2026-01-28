import httpx
from fastapi import APIRouter, Depends, HTTPException
from typing import Dict, Any
from app.schemas.kling import IdentifyFaceRequest, CreateSyncTaskRequest, TaskResponse
from app.services.kling_client import KlingClient, get_kling_client
import logging

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/api/v1/lipsync", tags=["Lip Sync"])

@router.post("/identify-face")
async def identify_face(request: IdentifyFaceRequest, client: KlingClient = Depends(get_kling_client)):
    """
    Identifies faces in a video. Returns session_id and face_data.
    This is a synchronous operation.
    """
    try:
        data = request.model_dump(mode='json', exclude_none=True)
        logger.info(f"Sending payload to Kling (Identify Face): {data}")
        
        response = await client.identify_face(data)
        
        logger.info(f"Received response from Kling (Identify Face): {response}")
        
        if response.get("code") != 0:
            raise HTTPException(status_code=400, detail=response.get("message", "Unknown error"))
        return response.get("data", {})
    except HTTPException:
        raise
    except httpx.HTTPStatusError as e:
        detail = e.response.text
        try:
            detail_json = e.response.json()
            detail = detail_json.get("message", detail)
            logger.error(f"Kling API Error (HTTP {e.response.status_code}): {detail}")
        except Exception:
            logger.error(f"Kling API Error (HTTP {e.response.status_code}): {detail}")
        raise HTTPException(status_code=e.response.status_code, detail=detail)
    except Exception as e:
        logger.error(f"Unexpected error: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/create-task", response_model=TaskResponse)
async def create_sync_task(request: CreateSyncTaskRequest, client: KlingClient = Depends(get_kling_client)):
    """
    Creates a lip sync task.
    """
    try:
        data = request.model_dump(mode='json', exclude_none=True)
        logger.info(f"Sending payload to Kling (Lip Sync): {data}")
        
        response = await client.create_lip_sync_task(data)
        
        logger.info(f"Received response from Kling (Lip Sync): {response}")
        
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
            logger.error(f"Kling API Error (HTTP {e.response.status_code}): {detail}")
        except Exception:
            logger.error(f"Kling API Error (HTTP {e.response.status_code}): {detail}")
        raise HTTPException(status_code=e.response.status_code, detail=detail)
    except Exception as e:
        logger.error(f"Unexpected error: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))
