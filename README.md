# Kling AI API Integration (FastAPI)

A high-performance FastAPI wrapper for the Kling AI Video Generation API. This project provides a structured, type-safe, and asynchronous interface for integrating Kling's Text-to-Video, Image-to-Video, Lip Sync, and Omni-Image generation capabilities.

## 🚀 Features

- **Full Async Support**: Built on `FastAPI` and `HTTPX` for high concurrency.
- **Type Safety**: Comprehensive `Pydantic` v2 models for all Requests and Responses.
- **Auto-Validation**: Automatic Base64 prefix cleaning and parameter validation.
- **Modular Design**: Separated Routers, Schemas, and Services.
- **Docker Ready**: Includes `Dockerfile` and `docker-compose.yml` for easy deployment.

## 🛠️ Prerequisites

- Python 3.9+
- Docker (Optional)

## 📦 Installation & Setup

1.  **Clone the repository**
    ```bash
    git clone <repository_url>
    cd langchain
    ```

2.  **Create a virtual environment**
    ```bash
    python -m venv venv
    # Windows
    .\venv\Scripts\activate
    # Linux/Mac
    source venv/bin/activate
    ```

3.  **Install dependencies**
    ```bash
    pip install -r requirements.txt
    ```

4.  **Configuration**
    Copy the example environment file and configure your API token:
    ```bash
    cp .env.example .env
    ```
    Edit `.env` and fill in your `KLING_AI_API_TOKEN`.

## 🚀 Running the Server

Start the development server with hot-reload:

```bash
uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

The server will start at `http://localhost:8000`.

## 📚 Documentation

- **Swagger UI**: Interactive API documentation is available at [http://localhost:8000/docs](http://localhost:8000/docs).
- **ReDoc**: Alternative documentation at [http://localhost:8000/redoc](http://localhost:8000/redoc).
- **TypeScript Types**: Frontend definitions are generated in `doc/api_types.ts`.

## 🧪 Testing

Run the test suite (including mocked API calls):

```bash
pytest
```

## 🐳 Docker Deployment

Build and run using Docker Compose:

```bash
docker-compose up -d --build
```

## 📂 Project Structure

```
.
├── app
│   ├── routers/      # API Routes (videos, images, lipsync, tasks)
│   ├── schemas/      # Pydantic Models & Validators
│   └── services/     # HTTP Client Wrapper
├── doc/              # Documentation & TS Types
├── tests/            # Unit Tests & Mocks
├── main.py           # Entry Point
├── Dockerfile
├── docker-compose.yml
└── requirements.txt
```
