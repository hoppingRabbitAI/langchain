from fastapi import APIRouter, Depends, HTTPException
from app.schemas.kling import GenerateImageRequest, OmniImageRequest, TaskResponse
from app.services.kling_client import KlingClient, get_kling_client

router = APIRouter(prefix="/api/v1/images", tags=["Image Generation"])

@router.post("/generations", response_model=TaskResponse)
async def generate_image(request: GenerateImageRequest, client: KlingClient = Depends(get_kling_client)):
    try:
        data = request.model_dump(mode='json', exclude_none=True)
        response = await client.generate_image(data)
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

@router.post("/omni-image", response_model=TaskResponse)
async def generate_omni(request: OmniImageRequest, client: KlingClient = Depends(get_kling_client)):
    try:
        data = request.model_dump(mode='json', exclude_none=True)
        response = await client.generate_omni_image(data)
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
