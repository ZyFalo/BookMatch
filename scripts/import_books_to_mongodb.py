#!/usr/bin/env python3
"""
Script para importar libros de Goodreads a la base de datos MongoDB de BookMatch
"""

import json
import os
import sys
import asyncio
from motor.motor_asyncio import AsyncIOMotorClient

# Usa la URI de MongoDB desde la configuración o variable de entorno
try:
    from app.config import MONGO_URL
except ImportError:
    MONGO_URL = os.environ.get("MONGO_URL", "mongodb://localhost:27017")

DB_NAME = "BMbackend"
COLLECTION_NAME = "books"

async def import_books_to_db(json_file):
    """Importa libros desde un archivo JSON a la colección books en MongoDB"""
    client = AsyncIOMotorClient(MONGO_URL)
    db = client[DB_NAME]
    books_collection = db[COLLECTION_NAME]

    # Leer el archivo JSON
    with open(json_file, 'r', encoding='utf-8') as f:
        books_data = json.load(f)

    # Limpiar y transformar los datos
    def clean_book(book):
        return {
            "titulo": book.get("titulo", ""),
            "autor": book.get("autor", ""),
            "portada": book.get("portada", ""),
            "resumen": book.get("resumen", ""),
            "tags": book.get("generos", []),
        }

    cleaned_books = [clean_book(b) for b in books_data]

    # Insertar en lotes
    if cleaned_books:
        result = await books_collection.insert_many(cleaned_books)
        print(f"Se importaron {len(result.inserted_ids)} libros a la base de datos")
    else:
        print("No se encontraron libros para importar")

if __name__ == "__main__":
    # Buscar el archivo JSON más reciente en la carpeta data
    data_dir = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "data")
    json_files = [f for f in os.listdir(data_dir) if f.startswith("goodreads_books_") and f.endswith(".json")]

    if not json_files:
        print("No se encontraron archivos de libros para importar")
        sys.exit(1)

    # Ordenar por fecha y tomar el más reciente
    latest_file = sorted(json_files)[-1]
    json_path = os.path.join(data_dir, latest_file)

    print(f"Importando libros desde: {json_path}")
    asyncio.run(import_books_to_db(json_path))