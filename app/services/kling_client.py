import httpx
import os
from typing import Any, Dict, Optional

class KlingClient:
    BASE_URL = "https://api.klingai.com/v1"

    def __init__(self, api_token: Optional[str] = None):
        self.api_token = api_token or os.getenv("KLING_AI_API_TOKEN")
        self.headers = {
            "Content-Type": "application/json",
        }
        if self.api_token:
            self.headers["Authorization"] = f"Bearer {self.api_token}"
        
        # Initialize client with timeout
        self.client = httpx.AsyncClient(
            base_url=self.BASE_URL, 
            headers=self.headers, 
            timeout=120.0 # Generative AI tasks might take time to submit or acknowledge? Usually submission is fast.
        )

    async def close(self):
        await self.client.aclose()

    async def _request(self, method: str, endpoint: str, **kwargs) -> Dict[str, Any]:
        try:
            response = await self.client.request(method, endpoint, **kwargs)
            response.raise_for_status()
            return response.json()
        except httpx.HTTPStatusError as e:
            # In a real app, we might want to parse the error response from Kling
            # and re-raise a custom exception or return the error details.
            # For now, we let the exception propagate or wrap it.
            raise e

    # --- Video Generation ---

    async def create_text2video(self, data: Dict[str, Any]) -> Dict[str, Any]:
        return await self._request("POST", "/videos/text2video", json=data)

    async def create_image2video(self, data: Dict[str, Any]) -> Dict[str, Any]:
        return await self._request("POST", "/videos/image2video", json=data)

    async def create_multi_image2video(self, data: Dict[str, Any]) -> Dict[str, Any]:
        return await self._request("POST", "/videos/multi-image2video", json=data)

    async def create_motion_control(self, data: Dict[str, Any]) -> Dict[str, Any]:
        return await self._request("POST", "/videos/motion-control", json=data)

    async def extend_video(self, data: Dict[str, Any]) -> Dict[str, Any]:
        return await self._request("POST", "/videos/video-extend", json=data)

    # --- Lip Sync ---

    async def identify_face(self, data: Dict[str, Any]) -> Dict[str, Any]:
        return await self._request("POST", "/videos/identify-face", json=data)

    async def create_lip_sync_task(self, data: Dict[str, Any]) -> Dict[str, Any]:
        return await self._request("POST", "/videos/advanced-lip-sync", json=data)

    # --- Image Generation ---

    async def generate_image(self, data: Dict[str, Any]) -> Dict[str, Any]:
        return await self._request("POST", "/images/generations", json=data)

    async def generate_omni_image(self, data: Dict[str, Any]) -> Dict[str, Any]:
        return await self._request("POST", "/images/omni-image", json=data)

    # --- Task Query ---

    async def get_task(self, endpoint_base: str, task_id: str) -> Dict[str, Any]:
        """
        Generic method to get task status.
        endpoint_base example: "/videos/text2video"
        """
        return await self._request("GET", f"{endpoint_base}/{task_id}")

    async def get_task_list(self, endpoint_base: str, page_num: int = 1, page_size: int = 30) -> Dict[str, Any]:
        params = {"pageNum": page_num, "pageSize": page_size}
        return await self._request("GET", endpoint_base, params=params)

# Dependency injection helper
_kling_client: Optional[KlingClient] = None

def get_kling_client() -> KlingClient:
    global _kling_client
    if _kling_client is None:
        _kling_client = KlingClient()
    return _kling_client
