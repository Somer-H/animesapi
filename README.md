# API Usuarios y Animes - FastAPI

Una API REST moderna con autenticación JWT, encriptación de contraseñas con bcrypt y arquitectura en capas.

## Características

**Autenticación JWT** - Tokens seguros en header Authorization  
**Encriptación bcrypt** - Contraseñas encriptadas  
**Arquitectura en capas** - Config, Models, Schemas, Repository, Service, Routes  
**Variables de entorno** - Usando .env y python-dotenv  
**Base de datos automática** - Las tablas se crean al iniciar la aplicación  
**2 Entidades** - Usuario y Anime  
**CRUD completo** - Crear, leer, actualizar, eliminar

## Instalación

### 1. Crear un entorno virtual
```bash
python -m venv venv
venv\Scripts\activate  # Windows
# source venv/bin/activate  # Mac/Linux
```

### 2. Instalar dependencias
```bash
pip install -r requirements.txt
```

### 3. Configurar variables de entorno
El archivo `.env` ya está configurado, pero puedes personalizarlo:
```env
DATABASE_URL=sqlite:///./api.db
SECRET_KEY=tu_clave_secreta_super_segura_cambiar_en_produccion_12345
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30
```

### 4. Ejecutar la API
```bash
python main.py
```

La API estará disponible en: `http://localhost:8000`

## Documentación Interactiva

- **Swagger UI**: http://localhost:8000/docs
- **ReDoc**: http://localhost:8000/redoc

## Endpoints

### Usuarios

#### 1. Registrarse
```http
POST /api/users/register
Content-Type: application/json

{
  "username": "juan",
  "email": "juan@example.com",
  "password": "micontraseña123"
}
```

**Respuesta:**
```json
{
  "id": 1,
  "username": "juan",
  "email": "juan@example.com",
  "created_at": "2024-02-04T10:30:00"
}
```

#### 2. Login
```http
POST /api/users/login
Content-Type: application/json

{
  "username": "juan",
  "password": "micontraseña123"
}
```

**Respuesta:**
```json
{
  "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
  "token_type": "bearer",
  "user": {
    "id": 1,
    "username": "juan",
    "email": "juan@example.com",
    "created_at": "2024-02-04T10:30:00"
  }
}
```

#### 3. Obtener usuario autenticado
```http
GET /api/users/me
Authorization: Bearer {access_token}
```

---

### Animes

#### 1. Crear anime (requiere autenticación)
```http
POST /api/animes
Authorization: Bearer {access_token}
Content-Type: application/json

{
  "titulo": "Attack on Titan",
  "genero": "Acción, Misterio",
  "año": 2013,
  "descripcion": "Un anime sobre titanes que devoran humanos"
}
```

#### 2. Obtener todos los animes
```http
GET /api/animes?skip=0&limit=10
```

#### 3. Obtener un anime por ID
```http
GET /api/animes/1
```

#### 4. Actualizar anime (requiere autenticación)
```http
PUT /api/animes/1
Authorization: Bearer {access_token}
Content-Type: application/json

{
  "titulo": "Attack on Titan S4",
  "año": 2020
}
```

#### 5. Eliminar anime (requiere autenticación)
```http
DELETE /api/animes/1
Authorization: Bearer {access_token}
```

## Estructura del Proyecto

```
api/
├── .env                          # Variables de entorno
├── main.py                       # Punto de entrada de la aplicación
├── requirements.txt              # Dependencias
│
├── config/                       # Configuración
│   ├── __init__.py
│   ├── settings.py              # Carga variables de entorno
│   └── database.py              # Configuración de BD y SQLAlchemy
│
├── security/                     # Autenticación y encriptación
│   ├── __init__.py
│   └── auth.py                  # JWT y bcrypt
│
├── user/                         # Módulo Usuario
│   ├── __init__.py
│   ├── models.py                # Modelo SQLAlchemy
│   ├── schemas.py               # Esquemas Pydantic
│   ├── repository.py            # Acceso a datos
│   ├── service.py               # Lógica de negocio
│   └── routes.py                # Endpoints
│
└── anime/                        # Módulo Anime
    ├── __init__.py
    ├── models.py                # Modelo SQLAlchemy
    ├── schemas.py               # Esquemas Pydantic
    ├── repository.py            # Acceso a datos
    ├── service.py               # Lógica de negocio
    └── routes.py                # Endpoints
```

## Flujo de Autenticación

1. Usuario se registra con **POST /api/users/register**
2. Usuario se autentica con **POST /api/users/login** (recibe token)
3. Usuario incluye el token en el header: `Authorization: Bearer {token}`
4. El servidor verifica el token y permite acceso a recursos protegidos

## Ejemplo con cURL

```bash
# Registrarse
curl -X POST "http://localhost:8000/api/users/register" \
  -H "Content-Type: application/json" \
  -d '{"username":"juan","email":"juan@example.com","password":"micontraseña123"}'

# Login
curl -X POST "http://localhost:8000/api/users/login" \
  -H "Content-Type: application/json" \
  -d '{"username":"juan","password":"micontraseña123"}'

# Obtener usuario autenticado
curl -X GET "http://localhost:8000/api/users/me" \
  -H "Authorization: Bearer {token}"

# Crear anime
curl -X POST "http://localhost:8000/api/animes" \
  -H "Authorization: Bearer {token}" \
  -H "Content-Type: application/json" \
  -d '{"titulo":"Death Note","genero":"Thriller","año":2006,"descripcion":"Un anime psicológico"}'
```



## Dependencias principales

- **FastAPI** - Framework web
- **SQLAlchemy** - ORM
- **Pydantic** - Validación de datos
- **python-jose** - JWT
- **passlib + bcrypt** - Encriptación de contraseñas
- **python-dotenv** - Variables de entorno
- **uvicorn** - Servidor ASGI
"# animesapi" 
