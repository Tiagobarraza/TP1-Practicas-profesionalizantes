from typing import Annotated
from fastapi import Depends, Body
from pydantic import BaseModel
from app.productos.dependencies import verify_api_token

# Esquema de producto
class Producto(BaseModel):
    nombre: str
    precio: float

# Dependencia inyectada para el token
TokenDep = Annotated[str, Depends(verify_api_token)]