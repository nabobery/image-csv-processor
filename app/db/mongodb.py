import motor.motor_asyncio
from app.core.config import get_settings
from app.core.logger import logger

client = None
db = None

settings = get_settings()

async def connect_to_mongo() -> None:
    global client, db
    client = motor.motor_asyncio.AsyncIOMotorClient(settings.mongodb_uri)
    db = client[settings.database_name]
    logger.info("Connected to MongoDB")

async def close_mongo_connection() -> None:
    global client
    if client:
        client.close()
        logger.info("MongoDB connection closed")

def get_collection(name: str):
    if db is None:
        raise Exception("Database not connected")
    return db[name]