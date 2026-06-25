from fastapi import FastAPI, Depends
from routers import usuarios, productos
from dependencies import verify_api_token

app = FastAPI(title="API de Usuarios y Productos")

# Incluir router de usuarios (sin protección)
app.include_router(usuarios.router)

# Incluir router de productos con protección GLOBAL
# ¡Todos los endpoints de /products necesitarán el token!
app.include_router(
    productos.router,
    dependencies=[Depends(verify_api_token)]
)

# Ruta raíz opcional
@app.get("/")
def home():
    return {"mensaje": "Bienvenido a la API. Usa /docs para ver la documentación."}
