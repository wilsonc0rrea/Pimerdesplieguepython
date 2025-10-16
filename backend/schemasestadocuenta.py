# backend/schemas.py
from pydantic import BaseModel
from typing import List, Optional
from datetime import datetime

# ✅ Campos comunes para creación y lectura (sin IDs ni fechas automáticas)
class EstadocuentaBase(BaseModel):
    estado: str

# ✅ Para CREAR cargo (cliente envía estos campos )
class EstadocuentaCreate(EstadocuentaBase):
    pass  # ← Hereda TODO de UserBase

# ✅ Para Update cargo (cliente envía estos campos )
class EstadocuentaUpdate(BaseModel):
    estado_id: int
    estado: str

# ✅ Para Update estado (cliente envía estos campos )
class EstadocuentaUpdateState(BaseModel):
    estado_id: int
    flag: bool

class DeleteEstadocuentaResponse(BaseModel):
    message: str

    class Config:
        from_attributes = True

# ✅ Para devolver
class Estadocuentas(EstadocuentaBase):
    estado_id: int
    flag: bool
    created_at: datetime  # importante para la respuesta
    updated_at: datetime  # importante para la respuesta

    class Config:
        from_attributes = True

# ✅ Para devolver respuesta con mensaje + cargo
class EstadocuentaResponse(BaseModel):
    message: str
    estadocuenta: Estadocuentas

    class Config:
        from_attributes = True