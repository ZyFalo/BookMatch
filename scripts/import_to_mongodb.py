#!/usr/bin/env python3
"""
Script para importar citas de Goodreads a la base de datos MongoDB de BookMatch
"""

import json
import os
import sys
import asyncio
from datetime import datetime
from motor.motor_asyncio import AsyncIOMotorClient
from bson import ObjectId

# Añadir el directorio raíz del proyecto al path para importar módulos
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from app.config import MONGO_URL

async def import_quotes_to_db(json_file):
    """Importa citas desde un archivo JSON a la colección quotes en MongoDB"""
    # Conectar a MongoDB
    client = AsyncIOMotorClient(MONGO_URL)
    db = client.BMbackend
    quotes_collection = db.quotes
    
    # Crear índices para búsqueda eficiente
    await quotes_collection.create_index([("tags", 1)])
    await quotes_collection.create_index([("author", 1)])
    
    # Leer el archivo JSON
    with open(json_file, 'r', encoding='utf-8') as f:
        quotes_data = json.load(f)
    
    # Transformar los datos para la base de datos
    quotes_for_db = []
    for quote in quotes_data:
        # Preparar el documento para MongoDB
        quote_doc = {
            "quote": quote["quote"],
            "author": quote["author"],
            "image_url": quote["image_url"],
            "tags": quote["tags"],
            "created_at": datetime.utcnow(),
            "source": "goodreads"
        }
        quotes_for_db.append(quote_doc)
    
    # Insertar en la base de datos
    if quotes_for_db:
        result = await quotes_collection.insert_many(quotes_for_db)
        print(f"Se importaron {len(result.inserted_ids)} citas a la base de datos")
    else:
        print("No se encontraron citas para importar")

if __name__ == "__main__":
    # Buscar el archivo JSON más reciente en la carpeta data
    data_dir = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "data")
    json_files = [f for f in os.listdir(data_dir) if f.startswith("goodreads_quotes_") and f.endswith(".json")]
    
    if not json_files:
        print("No se encontraron archivos de citas para importar")
        sys.exit(1)
    
    # Ordenar por fecha y tomar el más reciente
    latest_file = sorted(json_files)[-1]
    json_path = os.path.join(data_dir, latest_file)
    
    print(f"Importando citas desde: {json_path}")
    asyncio.run(import_quotes_to_db(json_path))