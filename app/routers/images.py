import httpx
from fastapi import APIRouter, Depends, HTTPException
from app.schemas.kling import GenerateImageRequest, OmniImageRequest, TaskResponse
from app.services.kling_client import KlingClient, get_kling_client
import logging

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/api/v1/images", tags=["Image Generation"])

@router.post("/generations", response_model=TaskResponse)
async def generate_image(request: GenerateImageRequest, client: KlingClient = Depends(get_kling_client)):
    try:
        data = request.model_dump(mode='json', exclude_none=True)
        logger.info(f"Sending payload to Kling (Generate Image): {data}")
        
        response = await client.generate_image(data)
        
        logger.info(f"Received response from Kling (Generate Image): {response}")
        
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

@router.post("/omni-image", response_model=TaskResponse)
async def generate_omni(request: OmniImageRequest, client: KlingClient = Depends(get_kling_client)):
    try:
        data = request.model_dump(mode='json', exclude_none=True)
        logger.info(f"Sending payload to Kling (Omni Image): {data}")

        response = await client.generate_omni_image(data)

        logger.info(f"Received response from Kling (Omni Image): {response}")

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
