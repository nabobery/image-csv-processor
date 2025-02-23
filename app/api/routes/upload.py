from fastapi import APIRouter, UploadFile, File, HTTPException
from app.services.csv_processor import process_csv_file
from app.schemas.response import UploadResponse
from app.core.logger import logger
import traceback

router = APIRouter()

@router.post("/upload", response_model=UploadResponse)
async def upload_csv(file: UploadFile = File(...)):
    if file.content_type != 'text/csv':
        logger.error(f"Invalid file type: {file.content_type}")
        raise HTTPException(status_code=400, detail="Only CSV files are allowed")
    
    try:
        request_id = await process_csv_file(file)
        logger.info(f"CSV processing started for request_id: {request_id}")
        return UploadResponse(request_id=request_id, message="Processing started")
    except HTTPException as e:
        raise HTTPException(status_code=e.status_code, detail=e.detail)
    except Exception as e:
        logger.error(f"Error processing CSV: {str(e)}\n{traceback.format_exc()}")
        raise HTTPException(status_code=500, detail=str(e))