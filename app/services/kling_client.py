import httpx
import os
import time
import jwt
from typing import Any, Dict, Optional

class KlingClient:
    # Default global BASE_URL. 
    # NOTE: If using Beijing node, set BASE_URL=https://api-beijing.klingai.com in .env (without /v1)
    # The client will append /v1 automatically or expect the user to provide the full base URL.
    # Based on the user's successful demo, the base URL is https://api-beijing.klingai.com
    # and endpoints are like /v1/videos/text2video.
    DEFAULT_BASE_URL = "https://api.klingai.com"

    def __init__(self, access_key: Optional[str] = None, secret_key: Optional[str] = None, base_url: Optional[str] = None):
        self.ak = access_key or os.getenv("KLING_ACCESS_KEY")
        self.sk = secret_key or os.getenv("KLING_SECRET_KEY")
        
        # Fallback to single token if AK/SK not provided (though AK/SK is recommended)
        self.static_token = os.getenv("KLING_AI_API_TOKEN")

        # Handle Base URL: ensure no trailing slash, and don't include /v1 yet if we want flexibility
        # But to match existing code logic, let's assume BASE_URL includes /v1 or we append it.
        # However, the user's demo uses `https://api-beijing.klingai.com` as base, and appends `/v1/...`
        # Our existing code uses `httpx.AsyncClient(base_url=...)` and then requests `/videos/...`.
        # So if base_url is `.../v1`, requesting `/videos/...` works.
        # If base_url is `.../`, requesting `/v1/videos/...` works.
        
        env_base_url = os.getenv("BASE_URL", self.DEFAULT_BASE_URL)
        self.base_url = base_url or env_base_url
        
        # Ensure base_url ends with /v1 to match our existing relative paths like "/videos/text2video"
        # OR we change all relative paths to include /v1.
        # Let's standardise: Base URL is the host. We append /v1 in requests OR Base URL includes /v1.
        # The user's error showed: POST https://api-beijing.klingai.com/videos/text2video -> 404.
        # This confirms that `https://api-beijing.klingai.com` requires `/v1` prefix.
        
        if not self.base_url.endswith("/v1"):
            self.base_url = f"{self.base_url}/v1"

        self.headers = {
            "Content-Type": "application/json",
        }
        
        self.client = httpx.AsyncClient(
            base_url=self.base_url, 
            headers=self.headers, 
            timeout=120.0
        )

    def _get_token(self) -> str:
        """
        Generates JWT token dynamically if AK/SK are present.
        Otherwise returns static token.
        """
        if self.ak and self.sk:
            headers = {
                "alg": "HS256",
                "typ": "JWT"
            }
            payload = {
                "iss": self.ak,
                "exp": int(time.time()) + 1800,  # 30 min validity
                "nbf": int(time.time()) - 5      # valid from 5s ago
            }
            token = jwt.encode(payload, self.sk, headers=headers)
            # PyJWT 2.x returns str, but just in case
            if isinstance(token, bytes):
                token = token.decode('utf-8')
            return token
        return self.static_token or ""

    async def close(self):
        await self.client.aclose()

    async def _request(self, method: str, endpoint: str, **kwargs) -> Dict[str, Any]:
        # Inject Authorization header dynamically for each request to ensure freshness
        token = self._get_token()
        if token:
            kwargs.setdefault("headers", {})["Authorization"] = f"Bearer {token}"
        
        try:
            response = await self.client.request(method, endpoint, **kwargs)
            response.raise_for_status()
            return response.json()
        except httpx.HTTPStatusError as e:
            # Re-raise to be handled by routers
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
