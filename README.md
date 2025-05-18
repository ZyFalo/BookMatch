# BookMatch

BookMatch es una aplicación web para gestionar y descubrir libros. Desarrollada con FastAPI para el backend y HTML/CSS/JavaScript para el frontend.

## Características

- Autenticación JWT
- API RESTful
- Frontend responsive
- Base de datos MongoDB

## Estructura del Proyecto

```
app/
  routes/
    item_routes.py
    user_routes.py
    __init__.py
  schemas/
    item_schema.py
    user_schema.py
    __init__.py
  services/
    item_service.py
    user_service.py
    __init__.py
  models/
    item_model.py
    user_model.py
    __init__.py
  db/
    database.py
    __init__.py
  static/
    css/
    js/
  templates/
  main.py
  config.py
  __init__.py
frontend/
  css/
  js/
  images/
tests/
  test_items.py
  test_users.py
  __init__.py
.env
.gitignore
requirements.txt
README.md
```

## Instalación

1. Clonar el repositorio:

```bash
git clone <repository-url>
cd BookMatch
```

2. Crear y activar entorno virtual:

```bash
python -m venv venv
# En Windows
venv\Scripts\activate
# En macOS/Linux
source venv/bin/activate
```

3. Instalar dependencias:

```bash
pip install -r requirements.txt
```

4. Configurar variables de entorno en el archivo `.env` (ya configurado).

## Ejecutar el Proyecto

```bash
uvicorn app.main:app --reload
```

La aplicación estará disponible en `http://localhost:8000`

## API Endpoints

### Autenticación

- `POST /api/token` - Obtener token JWT
- `POST /api/users/` - Registrar usuario

### Usuario

- `GET /api/users/me/` - Obtener información del usuario actual

### Libros

- `GET /api/books/` - Obtener lista de libros
- `GET /api/books/{book_id}` - Obtener un libro específico
- `POST /api/books/` - Crear un nuevo libro
- `PUT /api/books/{book_id}` - Actualizar un libro existente
- `DELETE /api/books/{book_id}` - Eliminar un libro

## Base de Datos

El proyecto utiliza MongoDB con las siguientes colecciones:
- books
- users
- interactions
- lists

## Probar con Postman

1. Registrar un usuario: `POST /api/users/`
   ```json
   {
     "username": "test_user",
     "email": "test@example.com",
     "full_name": "Test User",
     "password": "password123"
   }
   ```

2. Obtener token JWT: `POST /api/token`
   - Form data:
     - username: test_user
     - password: password123

3. Usar el token para acceder a los endpoints protegidos:
   - Headers:
     - Authorization: Bearer {token}