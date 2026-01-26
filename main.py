from fastapi import FastAPI, Request
from app.routers import videos, lipsync, images, tasks
from app.services.kling_client import get_kling_client
import logging

# Configure logger
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI(title="Kling AI API Integration", version="1.0.0")

app.include_router(videos.router)
app.include_router(lipsync.router)
app.include_router(images.router)
app.include_router(tasks.router)

@app.on_event("startup")
async def startup_event():
    # Initialize client
    get_kling_client()

@app.on_event("shutdown")
async def shutdown_event():
    client = get_kling_client()
    await client.close()

@app.get("/")
async def root():
    return {"message": "Welcome to Kling AI API Integration Service"}

@app.post("/callback")
async def handle_callback(request: Request):
    """
    Endpoint to receive asynchronous task updates from Kling AI.
    Configure this URL (publicly accessible) in your API calls as `callback_url`.
    """
    body = await request.json()
    logger.info(f"Received callback: {body}")
    # TODO: Implement your business logic here (e.g., update database, notify user)
    return {"status": "received"}
