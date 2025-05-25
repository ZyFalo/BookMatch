from fastapi import APIRouter, Request, Query, HTTPException
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse, JSONResponse
from bson import ObjectId
from app.db.mongo import db

router = APIRouter()
templates = Jinja2Templates(directory="app/templates")

@router.get("/books", response_class=HTMLResponse)
async def books_page(
    request: Request,
    page: int = Query(1, ge=1),
    q: str = Query("", alias="q")
):
    PAGE_SIZE = 12
    query = {}
    if q:
        query = {
            "$or": [
                {"titulo": {"$regex": q, "$options": "i"}},
                {"autor": {"$regex": q, "$options": "i"}}
            ]
        }
    total = await db.books.count_documents(query)
    books = await db.books.find(query).skip((page-1)*PAGE_SIZE).limit(PAGE_SIZE).to_list(PAGE_SIZE)
    # Limpiar y adaptar campos para la vista
    books_fmt = []
    for book in books:
        books_fmt.append({
            "id": str(book.get("_id")),
            "titulo": book.get("titulo", ""),
            "autor": book.get("autor", ""),
            "resumen": book.get("resumen", ""),
            "generos": book.get("generos", [])[:3],
            "detalle_url": book.get("detalle_url", ""),
            "portada": book.get("portada", "")
        })
    return templates.TemplateResponse("books.html", {
        "request": request,
        "books": books_fmt,
        "page": page,
        "pages": (total + PAGE_SIZE - 1) // PAGE_SIZE,
        "q": q
    })

@router.get("/books/{book_id}", response_class=HTMLResponse)
async def book_detail(request: Request, book_id: str):
    try:
        book = await db.books.find_one({"_id": ObjectId(book_id)})
    except Exception:
        book = None
    if not book:
        raise HTTPException(status_code=404, detail="Libro no encontrado")
    # Limpiar y adaptar campos para la vista
    book_fmt = {
        "id": str(book.get("_id")),
        "titulo": book.get("titulo", ""),
        "autor": book.get("autor", ""),
        "resumen": book.get("resumen", ""),
        "generos": book.get("generos", []),
        "detalle_url": book.get("detalle_url", ""),
        "portada": book.get("portada", "")
    }
    # Puedes agregar lógica para otros libros similares aquí si lo deseas
    return templates.TemplateResponse("books_info.html", {"request": request, "book": book_fmt})

@router.get("/books/{book_id}/similares")
async def books_similares(request: Request, book_id: str):
    try:
        book = await db.books.find_one({"_id": ObjectId(book_id)})
    except Exception:
        book = None
    if not book:
        raise HTTPException(status_code=404, detail="Libro no encontrado")
    criterios = []
    if book.get("autor"):
        criterios.append({"autor": book["autor"]})
    if book.get("titulo"):
        criterios.append({"titulo": {"$regex": book["titulo"].split()[0], "$options": "i"}})
    if book.get("generos"):
        criterios.append({"generos": {"$in": book["generos"]}})
    query = {"$or": criterios, "_id": {"$ne": book["_id"]}}
    similares = await db.books.aggregate([
        {"$match": query},
        {"$sample": {"size": 10}}
    ]).to_list(10)
    otros_libros = [{
        "id": str(b.get("_id")),
        "titulo": b.get("titulo", ""),
        "portada": b.get("portada", "")
    } for b in similares]
    return JSONResponse(content=otros_libros)