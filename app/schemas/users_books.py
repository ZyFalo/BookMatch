from pydantic import BaseModel
from typing import Optional

class InteractionCreate(BaseModel):
    book_id: str
    status: Optional[str] = "to-read"
    is_favorite: Optional[bool] = False
    rating: Optional[int] = None
    review: Optional[str] = None

class InteractionUpdate(BaseModel):
    status: Optional[str] = None
    is_favorite: Optional[bool] = None
    rating: Optional[int] = None
    review: Optional[str] = None