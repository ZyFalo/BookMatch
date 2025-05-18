from fastapi import APIRouter, Depends, HTTPException, Query
from typing import List, Optional
from app.db.mongo import get_database
from app.services.auth import get_current_user
from app.schemas.quotes import QuoteOut, QuoteFilter
from app.schemas.users import UserOut
import random

router = APIRouter()

@router.get("/recommendations", response_model=List[QuoteOut])
async def get_quote_recommendations(
    limit: int = Query(5, description="Número de citas a obtener"),
    current_user: UserOut = Depends(get_current_user)
):
    """
    Obtiene citas recomendadas basadas en las preferencias de tags del usuario.
    """
    db = await get_database()
    
    # Verificar si el usuario tiene preferencias de tags
    user_tags = []
    if hasattr(current_user, 'preferences') and current_user.preferences:
        user_tags = current_user.preferences.favorite_tags
    
    # Si no tiene tags favoritos, mostrar citas populares/aleatorias
    if not user_tags:
        # Obtener citas aleatorias
        cursor = db.quotes.aggregate([
            {"$sample": {"size": limit}}
        ])
        quotes = await cursor.to_list(length=limit)
    else:
        # Buscar citas que coincidan con los tags favoritos del usuario
        quotes = await db.quotes.find(
            {"tags": {"$in": user_tags}}
        ).limit(limit).to_list(length=limit)
        
        # Si no hay suficientes citas con esos tags, complementar con aleatorias
        if len(quotes) < limit:
            remaining = limit - len(quotes)
            # Excluir las citas ya seleccionadas
            existing_ids = [q["_id"] for q in quotes]
            random_quotes = await db.quotes.find(
                {"_id": {"$nin": existing_ids}}
            ).limit(remaining).to_list(length=remaining)
            
            quotes.extend(random_quotes)
    
    return quotes

@router.get("/daily", response_model=QuoteOut)
async def get_daily_quote(current_user: Optional[UserOut] = Depends(get_current_user)):
    """
    Obtiene la cita del día, personalizada si el usuario está autenticado.
    """
    db = await get_database()
    
    # Seleccionar tags para buscar
    tags = []
    if current_user and hasattr(current_user, 'preferences') and current_user.preferences:
        tags = current_user.preferences.favorite_tags
    
    # Buscar una cita que coincida con los tags del usuario o una aleatoria
    if tags:
        # Intentar encontrar citas con los tags del usuario
        quotes = await db.quotes.find({"tags": {"$in": tags}}).to_list(length=10)
        if quotes:
            return random.choice(quotes)
    
    # Si no hay coincidencias o el usuario no está autenticado, devolver una aleatoria
    cursor = db.quotes.aggregate([{"$sample": {"size": 1}}])
    quotes = await cursor.to_list(length=1)
    
    if not quotes:
        raise HTTPException(status_code=404, detail="No se encontraron citas")
    
    return quotes[0]

@router.get("/search", response_model=List[QuoteOut])
async def search_quotes(
    query: str = Query(None, description="Texto a buscar"),
    tag: str = Query(None, description="Tag para filtrar"), 
    author: str = Query(None, description="Autor para filtrar"),
    limit: int = Query(10, description="Número máximo de resultados")
):
    """
    Busca citas por texto, tag o autor.
    """
    db = await get_database()
    
    # Construir filtro según parámetros
    filter_query = {}
    
    if query:
        filter_query["$or"] = [
            {"quote": {"$regex": query, "$options": "i"}}, 
            {"author": {"$regex": query, "$options": "i"}}
        ]
    
    if tag:
        filter_query["tags"] = {"$in": [tag]}
    
    if author:
        filter_query["author"] = {"$regex": author, "$options": "i"}
    
    # Realizar búsqueda
    quotes = await db.quotes.find(filter_query).limit(limit).to_list(length=limit)
    
    return quotes

@router.get("/popular-tags", response_model=List[dict])
async def get_popular_tags(limit: int = Query(20, description="Número de tags a obtener")):
    """
    Obtiene los tags más populares para mostrar al usuario como sugerencias.
    """
    db = await get_database()
    
    # Agregar pipeline para calcular tags más frecuentes
    pipeline = [
        {"$unwind": "$tags"},
        {"$group": {"_id": "$tags", "count": {"$sum": 1}}},
        {"$sort": {"count": -1}},
        {"$limit": limit},
        {"$project": {"tag": "$_id", "count": 1, "_id": 0}}
    ]
    
    cursor = db.quotes.aggregate(pipeline)
    tags = await cursor.to_list(length=limit)
    
    return tags