import csv
import io
from uuid import uuid4
from fastapi import UploadFile, HTTPException
from app.db.mongodb import get_collection
from app.db.models import ProcessingRequest, Product
from app.services.image_processor import process_images
import asyncio
from app.core.logger import logger
import traceback

async def process_csv_file(file: UploadFile) -> str:
    try:
        content = await file.read()
        text_content = content.decode('utf-8')
        csv_reader = csv.DictReader(io.StringIO(text_content))
        
        products = []
        for row in csv_reader:
            # Validate required fields
            if not all(key in row for key in ['S. No.', 'Product Name', 'Input Image Urls']):
                logger.error(f"Missing required fields in CSV row: {row}")
                raise HTTPException(status_code=400, detail="Missing required fields in CSV")
            try:
                serial_number = int(row['S. No.'])
            except ValueError:
                logger.error(f"Invalid serial number format: {row['S. No.']}")
                raise HTTPException(status_code=400, detail="Invalid serial number format")
            
            product = Product(
                serial_number=serial_number,
                product_name=row['Product Name'],
                input_urls=row['Input Image Urls'].split(',')
            )
            products.append(product)
        
        request_id = str(uuid4())
        processing_request = ProcessingRequest(
            request_id=request_id,
            products=products
        )
        
        # Save to database
        collection = get_collection("requests")
        await collection.insert_one(processing_request.model_dump())
        
        logger.info(f"Created processing request: {request_id}")
        _ = asyncio.create_task(process_images(request_id))
        
        return request_id
    except HTTPException as e:
        raise HTTPException(status_code=e.status_code, detail=e.detail)
    except Exception as e:
        logger.error(f"Error processing CSV file: {str(e)}\n{traceback.format_exc()}")
        raise HTTPException(status_code=500, detail=str(e))