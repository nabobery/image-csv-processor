from pydantic import BaseModel, HttpUrl
from typing import List

class WebhookConfigRequest(BaseModel):
    webhook_url: HttpUrl
    events: List[str]