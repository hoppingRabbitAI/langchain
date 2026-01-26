# Kling AI API Callback Debugging Guide

Kling AI uses an asynchronous callback mechanism to notify your application when a video or image generation task is completed. This guide explains how to handle these callbacks and debug them locally.

## 1. How Callbacks Work

1.  **Request**: When you submit a task (e.g., `POST /videos/text2video`), you can optionally provide a `callback_url` parameter.
2.  **Processing**: Kling processes the task asynchronously.
3.  **Notification**: Once the task is finished (success or failure), Kling sends a `POST` request to your `callback_url` with the task results.

### Callback Payload Example

```json
{
  "task_id": "task_123456",
  "status": "succeed",
  "result": {
    "videos": [
      {
        "url": "https://cdn.klingai.com/...",
        "duration": "5"
      }
    ]
  }
}
```

## 2. Backend Implementation

We have implemented a basic callback handler in `main.py`:

```python
@app.post("/callback")
async def handle_callback(request: Request):
    body = await request.json()
    logger.info(f"Received callback: {body}")
    # TODO: Update database status, notify frontend via WebSocket, etc.
    return {"status": "received"}
```

## 3. Local Debugging with Ngrok

Since Kling's servers cannot reach your `localhost`, you need to expose your local server to the internet. **Ngrok** is the standard tool for this.

### Step-by-Step Guide

1.  **Install Ngrok**: Download from [ngrok.com](https://ngrok.com/download) and sign up.
2.  **Start your Local API**:
    ```bash
    uvicorn main:app --port 8000
    ```
3.  **Start Ngrok**:
    ```bash
    ngrok http 8000
    ```
    Ngrok will display a forwarding URL, e.g., `https://a1b2-c3d4.ngrok-free.app`.

4.  **Test the Callback**:
    *   **Method A (Manual Trigger)**: Use Postman or Curl to send a mock POST request to your local callback URL to verify your logic.
        ```bash
        curl -X POST http://localhost:8000/callback -d '{"task_id":"test", "status":"succeed"}'
        ```
    *   **Method B (Real API)**:
        *   Copy the Ngrok URL and append `/callback`.
        *   Example: `https://a1b2-c3d4.ngrok-free.app/callback`
        *   Use this URL as the `callback_url` parameter when calling `create_text2video` or other endpoints.

5.  **Check Logs**: Watch your terminal output (where `uvicorn` is running). You should see the `Received callback: ...` log message when Kling finishes the task.

## 4. Security Note

In production, you should verify that the callback request actually comes from Kling AI (if they provide signatures or IP whitelists) or use a secret token in the URL (e.g., `https://api.yoursite.com/callback?token=SECRET`).
