from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from user.routes import router as user_router
from anime.routes import router as anime_router

app = FastAPI(
    title="API Usuarios y Animes",
    description="API con autenticación JWT",
    version="1.0.0"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
    expose_headers=["Authorization"],
)

app.include_router(user_router)
app.include_router(anime_router)


@app.get("/")
def root():
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
    return {"status": "ok"}


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
