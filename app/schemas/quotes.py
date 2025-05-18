from pydantic import BaseModel, Field
from typing import List, Optional
from bson import ObjectId
from app.schemas.users import PyObjectId
from datetime import datetime

class QuoteBase(BaseModel):
    quote: str
    author: str
    image_url: Optional[str] = None
    tags: List[str] = Field(default_factory=list)

class QuoteCreate(QuoteBase):
    source: str = "manual"
    
class QuoteOut(QuoteBase):
    id: PyObjectId = Field(alias="_id")
    created_at: datetime
    source: str
    
    model_config = {
        "json_encoders": {ObjectId: str},
        "populate_by_name": True,
    }

class QuoteFilter(BaseModel):
    search: Optional[str] = None
    tag: Optional[str] = None
    author: Optional[str] = None