from enum import Enum
from pydantic import BaseModel
from typing import List, Optional

class ProcessingStatus(str, Enum):
    RECEIVED = "received"
    PROCESSING = "processing"
    COMPLETED = "completed"
    FAILED = "failed"

class Product(BaseModel):
    serial_number: int
    product_name: str
    input_urls: List[str]
    output_urls: Optional[List[str]] = []
    processing_status: Optional[ProcessingStatus] = ProcessingStatus.RECEIVED

class ProcessingRequest(BaseModel):
    request_id: str
    status: ProcessingStatus = ProcessingStatus.RECEIVED
    products: List[Product]
    csv_data: Optional[str] = None