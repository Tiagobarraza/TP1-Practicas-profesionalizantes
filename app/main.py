from fastapi import FastAPI, Depends
from app.usuarios.router import router as usuarios_router
from app.productos.router import router as productos_router
from app.productos.dependencies import verify_api_token # Asegúrate de importar esto

app = FastAPI()

# Incluir router de usuarios
app.include_router(usuarios_router)

# Incluir router de productos con la dependencia global
# Esta es la forma correcta de agrupar todo en una sola instrucción:
app.include_router(
    productos_router,
    dependencies=[Depends(verify_api_token)]
)

# Ruta raíz opcional
@app.get("/")
def home():
    return {"mensaje": "Bienvenido a la API. Usa /docs para ver la documentación."}