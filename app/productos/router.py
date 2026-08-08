from fastapi import APIRouter, Body, HTTPException
from typing import Annotated
from app.productos.schemas import Producto, TokenDep
from app.database import db_productos # O usa una lista local si no tienes database.py

# 1. El router tiene el prefijo "/products"
router = APIRouter(prefix="/products")

# 2. Ejercicio 3: Agregar producto (protegido por token, devuelve 201)
@router.post("/", status_code=201)
def agregar_producto(
    producto: Producto,
    token: TokenDep
):
    nuevo_producto = {"nombre": producto.nombre, "precio": producto.precio}
    db_productos.append(nuevo_producto)
    return {"mensaje": "Producto agregado", "producto": nuevo_producto}

# 3. Ejercicio 4: Listar productos (protegido por token)
@router.get("/")
def listar_productos(token: TokenDep):
    return {"productos": db_productos}