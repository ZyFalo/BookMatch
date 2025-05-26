from fastapi import APIRouter, HTTPException, Depends
from fastapi.responses import JSONResponse
from datetime import datetime
from bson import ObjectId
from app.db.mongo import db
from app.services.auth import get_current_user
from app.schemas.users_books import InteractionCreate, InteractionUpdate

router = APIRouter()

@router.post("/interactions/")
async def create_interaction(
    interaction: InteractionCreate,
    current_user=Depends(get_current_user)
):
    user_id = ObjectId(current_user["id"])
    book_obj_id = ObjectId(interaction.book_id)
    existing = await db.users_books.find_one({"user_id": user_id, "book_id": book_obj_id})
    if existing:
        raise HTTPException(status_code=400, detail="Interaction already exists")
    doc = {
        "user_id": user_id,
        "book_id": book_obj_id,
        "status": interaction.status,
        "is_favorite": interaction.is_favorite,
        "rating": interaction.rating,
        "review": interaction.review,
        "updated_at": datetime.utcnow()
    }
    await db.users_books.insert_one(doc)
    doc["user_id"] = str(doc["user_id"])
    doc["book_id"] = str(doc["book_id"])
    doc["updated_at"] = doc["updated_at"].isoformat()
    if "_id" in doc:
        doc["_id"] = str(doc["_id"])
    return JSONResponse(content=doc)

@router.get("/interactions/{book_id}")
async def get_interaction(book_id: str, current_user=Depends(get_current_user)):
    user_id = ObjectId(current_user["id"])
    book_obj_id = ObjectId(book_id)
    doc = await db.users_books.find_one({"user_id": user_id, "book_id": book_obj_id})
    if not doc:
        return JSONResponse(content=None, status_code=200)
    # Convertir todos los ObjectId a str para evitar errores de serialización
    doc["user_id"] = str(doc["user_id"])
    doc["book_id"] = str(doc["book_id"])
    if "_id" in doc:
        doc["_id"] = str(doc["_id"])
    if "updated_at" in doc:
        doc["updated_at"] = doc["updated_at"].isoformat()
    return JSONResponse(content=doc)

@router.patch("/interactions/{book_id}")
async def update_interaction(book_id: str, interaction: InteractionUpdate, current_user=Depends(get_current_user)):
    user_id = ObjectId(current_user["id"])
    book_obj_id = ObjectId(book_id)
    update_data = {"updated_at": datetime.utcnow()}
    if interaction.status is not None:
        update_data["status"] = interaction.status
    if interaction.is_favorite is not None:
        update_data["is_favorite"] = interaction.is_favorite
    if interaction.rating is not None:
        update_data["rating"] = interaction.rating
    if interaction.review is not None:
        update_data["review"] = interaction.review
    result = await db.users_books.update_one({"user_id": user_id, "book_id": book_obj_id}, {"$set": update_data})
    if result.matched_count == 0:
        raise HTTPException(status_code=404, detail="Interaction not found")
    doc = await db.users_books.find_one({"user_id": user_id, "book_id": book_obj_id})
    doc["user_id"] = str(doc["user_id"])
    doc["book_id"] = str(doc["book_id"])
    if "_id" in doc:
        doc["_id"] = str(doc["_id"])
    if "updated_at" in doc:
        doc["updated_at"] = doc["updated_at"].isoformat()
    return JSONResponse(content=doc)

@router.delete("/interactions/{book_id}")
async def delete_interaction(book_id: str, current_user=Depends(get_current_user)):
    user_id = ObjectId(current_user["id"])
    book_obj_id = ObjectId(book_id)
    result = await db.users_books.delete_one({"user_id": user_id, "book_id": book_obj_id})
    if result.deleted_count == 0:
        raise HTTPException(status_code=404, detail="Interaction not found")
    return {"detail": "Interaction deleted"}

@router.get("/interactions/")
async def get_all_interactions(current_user=Depends(get_current_user)):
    user_id = ObjectId(current_user["id"])
    interacciones = []
    async for doc in db.users_books.find({"user_id": user_id}):
        doc["user_id"] = str(doc["user_id"])
        doc["book_id"] = str(doc["book_id"])
        if "_id" in doc:
            doc["_id"] = str(doc["_id"])
        if "updated_at" in doc:
            doc["updated_at"] = doc["updated_at"].isoformat()
        interacciones.append(doc)
    return interacciones
