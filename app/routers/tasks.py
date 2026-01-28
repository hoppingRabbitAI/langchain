import httpx
from fastapi import APIRouter, Depends, HTTPException, Path
from app.schemas.kling import TaskResponse
from app.services.kling_client import KlingClient, get_kling_client

router = APIRouter(prefix="/api/v1/tasks", tags=["Task Query"])

@router.get("/{category}/{task_type}/{task_id}", response_model=TaskResponse)
async def get_task_status(
    category: str = Path(..., description="e.g. videos or images"),
    task_type: str = Path(..., description="e.g. text2video, generations"),
    task_id: str = Path(..., description="The task ID"),
    client: KlingClient = Depends(get_kling_client)
):
    """
    Unified task query interface.
    Path matches Kling API structure: /{category}/{task_type}/{task_id}
    Example: /videos/text2video/{id}
    """
    try:
        # Construct endpoint. e.g. /videos/text2video
        endpoint_base = f"/{category}/{task_type}"
        response = await client.get_task(endpoint_base, task_id)
        
        if response.get("code") != 0:
            raise HTTPException(status_code=400, detail=response.get("message", "Unknown error"))
            
        task_data = response.get("data", {})
        return TaskResponse(
            task_id=task_data.get("task_id", ""),
            message=task_data.get("task_status", "unknown"),
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
