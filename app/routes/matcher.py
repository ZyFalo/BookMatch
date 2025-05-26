from fastapi import APIRouter, Depends, Request
from app.services.user_match import match_usuarios
from app.db.mongo import get_db

router = APIRouter()

@router.post("/match")
async def match(request: Request, db=Depends(get_db)):
    """
    Endpoint para comparar la compatibilidad literaria entre dos usuarios por email.
    Recibe un JSON con email1 y email2.
    Devuelve un mensaje divertido y literario generado por Gemini.
    """
    data = await request.json()
    email1 = data.get("email1")
    email2 = data.get("email2")
    if not email1 or not email2:
        return {"error": "Debes enviar ambos correos electrónicos."}
    resultado = await match_usuarios(email1, email2, db)
    return resultado
