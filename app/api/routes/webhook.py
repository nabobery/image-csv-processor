from fastapi import APIRouter, HTTPException, Depends
from app.schemas.request import WebhookConfigRequest
from app.schemas.response import WebhookConfigResponse
from app.db.mongodb import get_collection
from app.core.security import verify_api_key
from app.core.logger import logger
import traceback

router = APIRouter()

@router.post("/configure", response_model=WebhookConfigResponse)
async def configure_webhook(config: WebhookConfigRequest, api_key: str = Depends(verify_api_key)):
    try:
        collection = get_collection("webhooks")
        # Upsert the webhook configuration and activate it.
        result = await collection.update_one(
            {},
            {"$set": {"webhook_url": config.webhook_url, "events": config.events, "active": True}},
            upsert=True
        )
        if result.modified_count == 0 and result.upserted_id is None:
            logger.error("Failed to configure webhook")
            raise HTTPException(status_code=500, detail="Failed to configure webhook")
        logger.info("Webhook configured successfully")
        return WebhookConfigResponse(message="Webhook configured successfully")
    except Exception as e:
        logger.error(f"Error configuring webhook: {str(e)}\n{traceback.format_exc()}")
        raise HTTPException(status_code=500, detail="Internal server error")