from fastapi import FastAPI, HTTPException, Request
import requests
from starlette.status import HTTP_401_UNAUTHORIZED
import os

app = FastAPI()

LLM_SERVICE_URL = "http://llm-service:8001"
API_KEYS = os.getenv("API_KEYS", "").split(",")

def check_api_key(request: Request):
    api_key = request.headers.get("X-API-Key")
    if api_key not in API_KEYS:
        raise HTTPException(status_code=HTTP_401_UNAUTHORIZED, detail="Invalid API Key")

@app.post("/process")
async def process_request(request: Request, body: dict):
    check_api_key(request)
    try:
        response = requests.post(f"{LLM_SERVICE_URL}/generate", json=body)
        return response.json()
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
