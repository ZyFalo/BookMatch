import requests
import google.generativeai as genai
import random
import os

GEMINI_API_URL = "https://generativelanguage.googleapis.com/v1beta/models/gemini-2.0-flash:generateContent?key=AIzaSyDQWd56NBG0B79C7La-4GdV3H2ElPBDaOc"

async def generar_recomendaciones(titulos_favoritos, db):
    """
    Genera 5 recomendaciones de libros usando Gemini,
    excluyendo los títulos favoritos del usuario y sugiriendo solo libros de la colección books.
    titulos_favoritos: lista de strings (títulos de libros favoritos)
    db: conexión a la base de datos MongoDB
    """
    # Obtener todos los títulos de la colección books que no estén en favoritos
    books_cursor = db.books.find({"titulo": {"$nin": titulos_favoritos}})
    books = await books_cursor.to_list(length=100)
    if not books:
        return "No hay suficientes libros en la base de datos para recomendar."
    # Selecciona hasta 30 títulos candidatos (aleatorio si hay muchos)
    candidatos = random.sample(books, min(30, len(books)))
    titulos_candidatos = [book["titulo"] for book in candidatos]
    # Prepara el prompt para Gemini
    prompt = (
        "Eres un recomendador de libros experto. Sugiere 4 libros de la lista de candidatos "
        "que podrían gustarle a un usuario, basándote en sus favoritos. Devuelve solo los títulos sugeridos, uno por línea, sin explicación extra.\n"
        f"Favoritos del usuario: {', '.join(titulos_favoritos)}\n"
        f"Candidatos: {', '.join(titulos_candidatos)}"
    )
    # Llamada directa a la API REST de Gemini
    payload = {
        "contents": [{"parts": [{"text": prompt}]}]
    }
    response = requests.post(GEMINI_API_URL, json=payload)
    if not response.ok:
        return f"Error al consultar Gemini: {response.text}"
    data = response.json()
    # Extraer la respuesta de Gemini
    try:
        gemini_text = data["candidates"][0]["content"]["parts"][0]["text"]
        sugerencias = [s.strip() for s in gemini_text.strip().splitlines() if s.strip()]
    except Exception:
        return "No se pudo interpretar la respuesta de Gemini."
    # Buscar los libros sugeridos en la base de datos y devolver su información completa
    sugeridos_cursor = db.books.find({"titulo": {"$in": sugerencias}})
    libros_sugeridos = await sugeridos_cursor.to_list(length=5)
    for libro in libros_sugeridos:
        libro["_id"] = str(libro["_id"])
    return libros_sugeridos