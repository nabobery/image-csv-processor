from pydantic_settings import BaseSettings
from functools import lru_cache

class Settings(BaseSettings):
    mongodb_uri: str = "mongodb://localhost:27017"
    database_name: str = "image_processing"
    api_key: str = "your_api_key"
    webhook_secret: str = "your_webhook_secret"
    image_storage_path: str = "images/"
    imgur_client_id: str
    
    class Config:
        env_file = ".env"
        case_sensitive = False

@lru_cache
def get_settings():
    return Settings()