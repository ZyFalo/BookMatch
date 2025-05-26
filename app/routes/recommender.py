from fastapi import APIRouter, Depends
from app.services.langchain_recommender import generar_recomendaciones
from app.db.mongo import get_db
from bson.objectid import ObjectId

router = APIRouter()

@router.get("/recomendar/{user_id}")
async def recomendar(user_id: str, db=Depends(get_db)):
    # Buscar los libros favoritos del usuario
    favoritos_cursor = db.users_books.find({
        "user_id": ObjectId(user_id),
        "is_favorite": True
    })
    favoritos = await favoritos_cursor.to_list(length=5)
    if not favoritos:
        return {"message": "No se encontraron libros favoritos."}

    # Obtener los títulos de los libros favoritos (usando 'titulo')
    book_ids = [fav["book_id"] for fav in favoritos]
    books_cursor = db.books.find({"_id": {"$in": book_ids}})
    books = await books_cursor.to_list(length=5)
    titulos = [book["titulo"] for book in books if "titulo" in book]

    if not titulos:
        return {"message": "No se encontraron títulos de libros favoritos."}

    sugeridos = await generar_recomendaciones(titulos, db)
    return {"recomendaciones": sugeridos}