from fastapi import APIRouter, Body, Depends
from pydantic import BaseModel
from typing import List, Annotated

# Importar la dependencia
from dependencies import verify_api_token

router = APIRouter(prefix="/products")

# Esquema de producto
class Producto(BaseModel):
    nombre: str
    precio: float

# Lista temporal de productos
db_productos = []

# Dependencia inyectada
TokenDep = Annotated[str, Depends(verify_api_token)]

# Ejercicio 3: Agregar producto (protegido por token)
@router.post("/", dependencies=[Depends(verify_api_token)])
def agregar_producto(
    nombre: Annotated[str, Body()],
    precio: Annotated[float, Body(gt=0)]
):
    nuevo_producto = {"nombre": nombre, "precio": precio}
    db_productos.append(nuevo_producto)
    return {"mensaje": "Producto agregado", "producto": nuevo_producto}

# Ejercicio 4: Listar productos (protegido por router completo)
@router.get("/")
def listar_productos():
    return {"productos": db_productos}
