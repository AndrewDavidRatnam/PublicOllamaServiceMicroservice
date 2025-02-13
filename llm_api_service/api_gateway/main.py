from fastapi import FastAPI, HTTPException, Request, Depends
import requests
from starlette.status import HTTP_401_UNAUTHORIZED
import os
import dotenv
import logging
import httpx
from fastapi.security import APIKeyHeader

app = FastAPI()
dotenv.load_dotenv()
API_KEYS = os.getenv("API_KEYS")
print(API_KEYS)
LLM_SERVICE_URL = "http://localhost:8001"
api_key_header = APIKeyHeader(name="API-Key")

def verify_api_key(api_key: str = Depends(api_key_header)):
    if api_key not in API_KEYS:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid API Key"
        )

@app.post("/process")
async def process_request(request: Request, api_key: str = Depends(verify_api_key)):
    try:
        body = await request.json()
        async with httpx.AsyncClient() as client:
            response = await client.post(f"{LLM_SERVICE_URL}/generate", json=body)
        response.raise_for_status()  # Raises an exception for 4xx/5xx responses
        return response.json()
    except httpx.HTTPStatusError as e:
        raise HTTPException(status_code=e.response.status_code, detail=e.response.text)
    except httpx.RequestError as e:
        raise HTTPException(status_code=500, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail="An unexpected error occurred")
