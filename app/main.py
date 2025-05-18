from fastapi import FastAPI, Request, Depends, HTTPException
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse
from fastapi.middleware.cors import CORSMiddleware
from app.routes.users import router as user_router
from app.db.mongo import check_connection, startup_db_client

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

# Ruta para comprobar el estado de la API
@app.get("/api/health")
async def health_check():
    is_db_connected = await check_connection()
    return {
        "status": "ok" if is_db_connected else "error",
        "database": "connected" if is_db_connected else "disconnected"
    }

# Ruta para comprobar el estado de la API sin bloquear
@app.get("/api/quick-health")
def quick_health_check():
    return {"status": "running", "message": "API funcionando correctamente"}

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