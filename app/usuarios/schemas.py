from typing import Annotated
from fastapi import Body
from pydantic import BaseModel

# Esquema de usuario básico
class Usuario(BaseModel):
    username: str
    edad: int

# Validaciones con Annotated
UsernameAnnotated = Annotated[str, Body(min_length=5)]
EdadAnnotated = Annotated[int, Body(ge=18)]