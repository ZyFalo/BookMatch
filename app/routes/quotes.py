from fastapi import APIRouter, HTTPException
from app.db.mongo import db
import random

router = APIRouter()

@router.get("/random", response_model=dict)
async def get_random_quote():
    count = await db.quotes.count_documents({})
    if count == 0:
        raise HTTPException(status_code=404, detail="No quotes found")
    rand_index = random.randint(0, count - 1)
    quote = await db.quotes.find().skip(rand_index).limit(1).to_list(1)
    if not quote:
        raise HTTPException(status_code=404, detail="No quote found")
    q = quote[0]
    # Eliminar o convertir el _id
    q.pop("_id", None)  # Elimina el campo _id
    q["image_url"] = q.get("image_url") or "/static/img/authors/default.webp"
    return {
        "quote": q.get("quote", ""),
        "author": q.get("author", ""),
        "image_url": q["image_url"]
    }