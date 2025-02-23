from fastapi import APIRouter, HTTPException
from app.db.mongodb import get_collection
from app.schemas.response import StatusResponse
from app.core.logger import logger
import traceback

router = APIRouter()

@router.get("/status/{request_id}", response_model=StatusResponse)
async def get_status(request_id: str):
    try:
        collection = get_collection("requests")
        request = await collection.find_one({"request_id": request_id})
        
        if not request:
            logger.error(f"Request not found: {request_id}")
            raise HTTPException(status_code=404, detail="Request not found")
            
        logger.info(f"Retrieved status for request: {request_id}")
        return StatusResponse(**request)
    except Exception as e:
        logger.error(f"Error retrieving status for request {request_id}: {str(e)}\n{traceback.format_exc()}")
        raise HTTPException(status_code=500, detail="Internal server error")