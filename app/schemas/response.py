from pydantic import BaseModel
from typing import List, Optional

class UploadResponse(BaseModel):
    request_id: str
    message: str

class ProductResponse(BaseModel):
    serial_number: int
    product_name: str
    input_urls: List[str]
    output_urls: Optional[List[str]] = None
    processing_status: str

class StatusResponse(BaseModel):
    request_id: str
    status: str
    products: List[ProductResponse]

class WebhookConfigResponse(BaseModel):
    message: str