from fastapi import APIRouter, HTTPException, Body, Path, Query
from pydantic import BaseModel
from typing import List, Annotated

router = APIRouter(prefix="/users")

# Base de datos temporal
db_usuarios = []

# Esquema de usuario
class Usuario(BaseModel):
    username: str
    edad: int

# Validaciones con Annotated
UsernameAnnotated = Annotated[str, Body(min_length=5)]
EdadAnnotated = Annotated[int, Body(ge=18)]

# Ejercicio 1: Registro de usuario
@router.post("/")
def registrar_usuario(
    username: UsernameAnnotated,
    edad: EdadAnnotated
):
    # Verificar si ya existe
    for u in db_usuarios:
        if u["username"] == username:
            raise HTTPException(status_code=400, detail="Usuario ya existe")
    
    nuevo_usuario = {"username": username, "edad": edad}
    db_usuarios.append(nuevo_usuario)
    return {"mensaje": "Usuario registrado", "usuario": nuevo_usuario}

# Ejercicio 2: Búsqueda por ID
@router.get("/{user_id}")
def buscar_usuario(
    user_id: Annotated[int, Path(gt=0)],
    categoria: Annotated[str, Query(min_length=3)] = "general"
):
    if user_id > len(db_usuarios) or user_id <= 0:
        raise HTTPException(status_code=404, detail="Usuario no encontrado")
    
    usuario = db_usuarios[user_id - 1]  # ID empieza en 1, lista en 0
    return {
        "usuario": usuario,
        "categoria": categoria
    }
