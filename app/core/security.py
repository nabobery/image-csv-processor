from fastapi import Header, HTTPException
from app.core.config import get_settings

settings = get_settings()

async def verify_api_key(x_api_key: str = Header(...)) -> str:
    if x_api_key != settings.api_key:
        raise HTTPException(status_code=403, detail="Invalid API Key")
    return x_api_key