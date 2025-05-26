import requests
import random

GEMINI_API_URL = "https://generativelanguage.googleapis.com/v1beta/models/gemini-2.0-flash:generateContent?key=AIzaSyDQWd56NBG0B79C7La-4GdV3H2ElPBDaOc"

async def match_usuarios(email1, email2, db):
    """
    Calcula la compatibilidad literaria entre dos usuarios usando Gemini.
    Devuelve un mensaje divertido y literario sobre la compatibilidad.
    """
    # Buscar usuarios
    user1 = await db.users.find_one({"email": email1})
    user2 = await db.users.find_one({"email": email2})
    if not user1 or not user2:
        return {"error": "Uno o ambos usuarios no existen."}
    # Buscar libros favoritos de cada usuario
    favs1_cursor = db.users_books.find({"user_id": user1["_id"], "is_favorite": True})
    favs2_cursor = db.users_books.find({"user_id": user2["_id"], "is_favorite": True})
    favs1 = await favs1_cursor.to_list(length=5)
    favs2 = await favs2_cursor.to_list(length=5)
    # Obtener títulos
    ids1 = [f["book_id"] for f in favs1]
    ids2 = [f["book_id"] for f in favs2]
    books1 = await db.books.find({"_id": {"$in": ids1}}).to_list(length=5)
    books2 = await db.books.find({"_id": {"$in": ids2}}).to_list(length=5)
    titulos1 = [b["titulo"] for b in books1 if "titulo" in b]
    titulos2 = [b["titulo"] for b in books2 if "titulo" in b]
    # Prepara el prompt
    prompt = (
        f"Imagina que eres un cupido literario. Analiza la compatibilidad entre dos lectores basándote en sus libros favoritos. "
        f"Sé divertido, literario y un poco bromista. ¿Son almas gemelas de la literatura o rivales de estantería?\n"
        f"Usuario 1 ({user1.get('username','sin nombre')}): {', '.join(titulos1) if titulos1 else 'sin favoritos'}\n"
        f"Usuario 2 ({user2.get('username','sin nombre')}): {', '.join(titulos2) if titulos2 else 'sin favoritos'}\n"
        "Devuelve solo un mensaje creativo y literario, no una lista de libros."
    )
    payload = {
        "contents": [{"parts": [{"text": prompt}]}]
    }
    response = requests.post(GEMINI_API_URL, json=payload)
    if not response.ok:
        return {"error": f"Error al consultar Gemini: {response.text}"}
    data = response.json()
    try:
        gemini_text = data["candidates"][0]["content"]["parts"][0]["text"]
    except Exception:
        return {"error": "No se pudo interpretar la respuesta de Gemini."}
    return {"mensaje": gemini_text.strip()}
