from fastapi import FastAPI, Request, Depends, HTTPException
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse
from fastapi.middleware.cors import CORSMiddleware
from app.routes.users import router as user_router
from app.db.mongo import check_connection, startup_db_client
from app.services.auth import get_current_user

app = FastAPI(title="BookMatch API")

# Configurar CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # En producción, especifica los dominios permitidos
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Evento de arranque para inicializar la base de datos
@app.on_event("startup")
async def on_startup():
    await startup_db_client()

# Montar archivos estáticos
app.mount("/static", StaticFiles(directory="app/static"), name="static")

# Configurar templates
templates = Jinja2Templates(directory="app/templates")

# Incluir rutas de la API
app.include_router(user_router, prefix="/users", tags=["users"])

# Rutas principales para servir las páginas HTML
@app.get("/", response_class=HTMLResponse)
async def read_root(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})

@app.get("/login", response_class=HTMLResponse)
async def read_login(request: Request):
    return templates.TemplateResponse("login.html", {"request": request})

@app.get("/profile", response_class=HTMLResponse)
async def profile_page(request: Request):
    return templates.TemplateResponse("profile.html", {"request": request})

# Ruta para pruebas de validación de esquemas
@app.post("/api/debug/validate")
async def debug_validation(request: Request):
    try:
        # Recibir el cuerpo de la petición como JSON
        raw_data = await request.json()
        return {
            "received_data": raw_data,
            "validation": "success"
        }
    except Exception as e:
        return {
            "error": str(e),
            "validation": "failed"
        }