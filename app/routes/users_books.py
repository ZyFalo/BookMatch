from fastapi import APIRouter, HTTPException, Depends
from fastapi.responses import JSONResponse
from datetime import datetime
from bson import ObjectId
from app.db.mongo import db
from app.services.auth import get_current_user

router = APIRouter()

@router.post("/interactions/")
async def create_interaction(book_id: str, status: str = "to-read", is_favorite: bool = False, rating: int = None, review: str = None, current_user=Depends(get_current_user)):
    user_id = ObjectId(current_user["id"])
    book_obj_id = ObjectId(book_id)
    existing = await db.users_books.find_one({"user_id": user_id, "book_id": book_obj_id})
    if existing:
        raise HTTPException(status_code=400, detail="Interaction already exists")
    doc = {
        "user_id": user_id,
        "book_id": book_obj_id,
        "status": status,
        "is_favorite": is_favorite,
        "rating": rating,
        "review": review,
        "updated_at": datetime.utcnow()
    }
    await db.users_books.insert_one(doc)
    doc["user_id"] = str(doc["user_id"])
    doc["book_id"] = str(doc["book_id"])
    return JSONResponse(content=doc)

@router.get("/interactions/{book_id}")
async def get_interaction(book_id: str, current_user=Depends(get_current_user)):
    user_id = ObjectId(current_user["id"])
    book_obj_id = ObjectId(book_id)
    doc = await db.users_books.find_one({"user_id": user_id, "book_id": book_obj_id})
    if not doc:
        raise HTTPException(status_code=404, detail="Interaction not found")
    doc["user_id"] = str(doc["user_id"])
    doc["book_id"] = str(doc["book_id"])
    return JSONResponse(content=doc)

@router.patch("/interactions/{book_id}")
async def update_interaction(book_id: str, status: str = None, is_favorite: bool = None, rating: int = None, review: str = None, current_user=Depends(get_current_user)):
    user_id = ObjectId(current_user["id"])
    book_obj_id = ObjectId(book_id)
    update_data = {"updated_at": datetime.utcnow()}
    if status is not None:
        update_data["status"] = status
    if is_favorite is not None:
        update_data["is_favorite"] = is_favorite
    if rating is not None:
        update_data["rating"] = rating
    if review is not None:
        update_data["review"] = review
    result = await db.users_books.update_one({"user_id": user_id, "book_id": book_obj_id}, {"$set": update_data})
    if result.matched_count == 0:
        raise HTTPException(status_code=404, detail="Interaction not found")
    doc = await db.users_books.find_one({"user_id": user_id, "book_id": book_obj_id})
    doc["user_id"] = str(doc["user_id"])
    doc["book_id"] = str(doc["book_id"])
    return JSONResponse(content=doc)

@router.delete("/interactions/{book_id}")
async def delete_interaction(book_id: str, current_user=Depends(get_current_user)):
    user_id = ObjectId(current_user["id"])
    book_obj_id = ObjectId(book_id)
    result = await db.users_books.delete_one({"user_id": user_id, "book_id": book_obj_id})
    if result.deleted_count == 0:
        raise HTTPException(status_code=404, detail="Interaction not found")
    return {"detail": "Interaction deleted"}
