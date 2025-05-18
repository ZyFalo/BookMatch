from fastapi import APIRouter, HTTPException, Depends, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from app.db.mongo import db
from app.schemas.users import UserCreate, UserOut, UserLogin, UserResponse, UserUpdate
from app.services.auth import hash_password, verify_password, create_access_token, get_current_user
from bson import ObjectId

router = APIRouter()
templates = Jinja2Templates(directory="app/templates")

@router.post("/register", response_model=UserOut)
async def register(user: UserCreate):
    # Verificar si el email ya está registrado
    email_exists = await db.users.find_one({"email": user.email})
    if email_exists:
        raise HTTPException(status_code=400, detail="Email already registered")
    
    # Verificar si el username ya está en uso
    username_exists = await db.users.find_one({"username": user.username})
    if username_exists:
        raise HTTPException(status_code=400, detail="Username already taken")
    
    hashed = hash_password(user.password)
    result = await db.users.insert_one({
        "username": user.username,
        "full_name": user.full_name,
        "email": user.email,
        "password": hashed,
    })
    created_user = await db.users.find_one({"_id": result.inserted_id})
    return UserOut(**created_user)

@router.post("/login")
async def login(user: UserLogin):
    db_user = await db.users.find_one({"email": user.email})
    if not db_user or not verify_password(user.password, db_user["password"]):
        raise HTTPException(status_code=401, detail="Invalid credentials")

    token = create_access_token({"sub": str(db_user["_id"])})
    return {"access_token": token, "token_type": "bearer"}

@router.get("/me", response_model=UserResponse)
async def get_current_user_info(current_user = Depends(get_current_user)):
    """Obtiene información del usuario actualmente autenticado"""
    return current_user

@router.put("/update-profile", response_model=UserResponse)
async def update_profile(user_update: UserUpdate, current_user = Depends(get_current_user)):
    """Actualiza la información del perfil del usuario"""
    user_id = current_user.get("id")
    
    # Verificar si el username ya está en uso (si está cambiando)
    if user_update.username != current_user.get("username"):
        username_exists = await db.users.find_one({"username": user_update.username, "_id": {"$ne": ObjectId(user_id)}})
        if username_exists:
            raise HTTPException(status_code=400, detail="Username already taken")
    
    # Verificar contraseña actual si está cambiando la contraseña
    if user_update.new_password:
        if not user_update.current_password:
            raise HTTPException(status_code=400, detail="Current password is required")
        
        user_with_pwd = await db.users.find_one({"_id": ObjectId(user_id)})
        if not verify_password(user_update.current_password, user_with_pwd["password"]):
            raise HTTPException(status_code=400, detail="Current password is incorrect")
    
    # Preparar datos de actualización
    update_data = {
        "username": user_update.username,
        "full_name": user_update.full_name,
    }
    
    # Si hay cambio de contraseña, actualizar hash
    if user_update.new_password:
        update_data["password"] = hash_password(user_update.new_password)
    
    # Actualizar en la base de datos
    await db.users.update_one(
        {"_id": ObjectId(user_id)},
        {"$set": update_data}
    )
    
    # Obtener el usuario actualizado
    updated_user = await db.users.find_one({"_id": ObjectId(user_id)})
    updated_user["id"] = str(updated_user["_id"])
    
    # Eliminar la contraseña del resultado
    if "password" in updated_user:
        del updated_user["password"]
    
    return updated_user

@router.get("/profile", response_class=HTMLResponse)
async def profile_page(request: Request, current_user = Depends(get_current_user)):
    """Renderiza la página de perfil del usuario"""
    if not current_user:
        return templates.TemplateResponse("login.html", {"request": request})
    
    return templates.TemplateResponse("profile.html", {"request": request, "user": current_user})
