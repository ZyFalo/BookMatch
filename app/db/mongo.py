from motor.motor_asyncio import AsyncIOMotorClient
from app.config import MONGO_URL
import asyncio

# Configurar cliente MongoDB con timeouts razonables
client = AsyncIOMotorClient(MONGO_URL, serverSelectionTimeoutMS=5000)
db = client.BMbackend

# Función para verificar conexión
async def check_connection():
    try:
        await client.admin.command('ping')
        return True
    except Exception as e:
        print(f"Error de conexión a MongoDB: {e}")
        return False

# Función para inicializar índices en la base de datos
async def init_db():
    try:
        # Crear índice único para email
        await db.users.create_index("email", unique=True)
        
        # Crear índice único para username
        await db.users.create_index("username", unique=True)
        
        # Crear otros índices útiles
        await db.books.create_index("title")
        await db.books.create_index("author")
        
        print("Índices de base de datos inicializados correctamente")
    except Exception as e:
        print(f"Error al inicializar índices: {e}")

# Ejecutar esta función al iniciar la aplicación
async def startup_db_client():
    if await check_connection():
        await init_db()
    else:
        print("No se pudo conectar a MongoDB para inicializar índices")
