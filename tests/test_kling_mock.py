import os
import sys
import pytest
from unittest.mock import AsyncMock, patch
from fastapi.testclient import TestClient

PROJECT_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
if PROJECT_ROOT not in sys.path:
    sys.path.insert(0, PROJECT_ROOT)

from main import app
from app.services.kling_client import get_kling_client, KlingClient
from tests.mock_kling_response import (
    MOCK_TEXT2VIDEO_RESPONSE, 
    MOCK_TASK_QUERY_SUCCESS,
    MOCK_LIPSYNC_IDENTIFY_RESPONSE
)

client = TestClient(app)

# --- Dependency Override for Mocking ---
# We will mock the KlingClient's methods directly.

@pytest.fixture
def mock_kling_client():
    mock_client = AsyncMock(spec=KlingClient)
    # Setup return values for common methods
    mock_client.create_text2video.return_value = MOCK_TEXT2VIDEO_RESPONSE
    mock_client.get_task.return_value = MOCK_TASK_QUERY_SUCCESS
    mock_client.identify_face.return_value = MOCK_LIPSYNC_IDENTIFY_RESPONSE
    return mock_client

@pytest.fixture
def override_dependency(mock_kling_client):
    app.dependency_overrides[get_kling_client] = lambda: mock_kling_client
    yield
    app.dependency_overrides = {}

# --- Tests ---

def test_create_text2video(override_dependency, mock_kling_client):
    payload = {
        "prompt": "A cinematic shot of a cyberpunk city",
        "model_name": "kling-v1",
        "aspect_ratio": "16:9"
    }
    response = client.post("/api/v1/videos/text2video", json=payload)
    
    # Assert HTTP Status
    assert response.status_code == 200
    
    # Assert Response Body
    data = response.json()
    assert data["task_id"] == "task_t2v_001"
    assert data["message"] == "success"
    
    # Assert Mock was called correctly
    mock_kling_client.create_text2video.assert_called_once()
    # Verify arguments passed to client method (should be dict)
    call_args = mock_kling_client.create_text2video.call_args[0][0]
    assert call_args["prompt"] == payload["prompt"]
    assert call_args["model_name"] == payload["model_name"]

def test_get_task_status(override_dependency, mock_kling_client):
    task_id = "task_t2v_001"
    response = client.get(f"/api/v1/tasks/videos/text2video/{task_id}")
    
    assert response.status_code == 200
    data = response.json()
    assert data["task_id"] == task_id
    assert data["message"] == "succeed"
    assert data["raw_data"]["task_result"]["videos"][0]["url"] == "https://cdn.klingai.com/videos/generated_001.mp4"
    
    mock_kling_client.get_task.assert_called_once_with("/videos/text2video", task_id)

def test_identify_face(override_dependency, mock_kling_client):
    payload = {"video_url": "https://example.com/video.mp4"}
    response = client.post("/api/v1/lipsync/identify-face", json=payload)
    
    assert response.status_code == 200
    data = response.json()
    assert data["session_id"] == "sess_001"
    assert len(data["face_data"]) == 1
    
    mock_kling_client.identify_face.assert_called_once()
