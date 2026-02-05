from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from config.database import create_tables
from user.routes import router as user_router
from anime.routes import router as anime_router

# Crear la aplicación FastAPI
app = FastAPI(
    title="API Usuarios y Animes",
    description="API con autenticación JWT",
    version="1.0.0"
)

# Configurar CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Crear las tablas al iniciar
@app.on_event("startup")
def startup_event():
    """Crea las tablas de la base de datos al iniciar la aplicación"""
    create_tables()
    print("Tablas de base de datos creadas correctamente")


# Incluir routers
app.include_router(user_router)
app.include_router(anime_router)


@app.get("/")
def root():
    """Endpoint raíz"""
    return {
        "mensaje": "Bienvenido a la API",
        "documentación": "/docs",
        "endpoints": {
            "registro": "POST /api/users/register",
            "login": "POST /api/users/login",
            "usuario_actual": "GET /api/users/me",
            "animes": "GET /api/animes",
            "crear_anime": "POST /api/animes",
            "obtener_anime": "GET /api/animes/{id}",
            "actualizar_anime": "PUT /api/animes/{id}",
            "eliminar_anime": "DELETE /api/animes/{id}"
        }
    }


@app.get("/health")
def health_check():
    """Health check endpoint"""
    return {"status": "ok"}


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
