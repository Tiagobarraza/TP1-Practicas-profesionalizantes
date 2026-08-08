from typing import Annotated
from fastapi import APIRouter, HTTPException, Path, Query
from app.usuarios.schemas import UsernameAnnotated, EdadAnnotated
from app.database import db_usuarios

# El router DEBE tener el prefijo "/users"
router = APIRouter(prefix="/users")

# Ejercicio 1: Registro de usuario (Devuelve 201 en éxito)
@router.post("/", status_code=201)
def registrar_usuario(username: UsernameAnnotated, edad: EdadAnnotated):
    
    # Verificar si ya existe el usuario
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