import json
import requests
from bs4 import BeautifulSoup
import time
import os

# Ruta correcta al JSON de libros (relativa al script)
json_path = os.path.join(os.path.dirname(__file__), '..', 'data', 'goodreads_books_1748131063.json')
json_path = os.path.abspath(json_path)

# Cargar los libros
with open(json_path, 'r', encoding='utf-8') as f:
    libros = json.load(f)

# Procesar todos los libros (sin límite)
for i, libro in enumerate(libros):
    print(f"Reemplazando imagen: {i+1} de {len(libros)}")
    url = libro.get("detalle_url")
    imagen_url = ""
    if url:
        try:
            r = requests.get(url, timeout=10)
            soup = BeautifulSoup(r.text, 'html.parser')
            meta_img = soup.find('meta', property='og:image')
            if meta_img and meta_img.get("content"):
                imagen_url = meta_img["content"]
        except Exception:
            pass
    libro["portada"] = imagen_url  # Vacío si no hay imagen o ruta

    time.sleep(1)  # evitar bloqueo por demasiadas peticiones

output_path = os.path.join(os.path.dirname(__file__), '..', 'data', 'goodreads_books_con_imagenes.json')
output_path = os.path.abspath(output_path)
with open(output_path, 'w', encoding='utf-8') as f:
    json.dump(libros, f, ensure_ascii=False, indent=2)