import aiohttp
from app.db.mongodb import get_collection
from app.core.logger import logger
import traceback

async def send_webhook_notification(request_id: str):
    try:
        collection = get_collection("webhooks")
        webhook_config = await collection.find_one({"active": True})
        
        if not webhook_config:
            logger.warning("No active webhook configuration found")
            return
            
        request_collection = get_collection("requests")
        request_data = await request_collection.find_one({"request_id": request_id})
        
        if not request_data:
            logger.error(f"Request data not found for request_id: {request_id}")
            return
            
        async with aiohttp.ClientSession() as session:
            await session.post(
                webhook_config["webhook_url"],
                json={
                    "request_id": request_id,
                    "status": request_data["status"],
                    "event": "processing.completed"
                }
            )
        logger.info(f"Webhook notification sent for request_id: {request_id}")
    except Exception as e:
        logger.error(f"Error sending webhook notification: {str(e)}\n{traceback.format_exc()}")