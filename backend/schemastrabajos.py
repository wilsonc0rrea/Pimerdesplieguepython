# backend/schemas.py
from pydantic import BaseModel
from typing import List, Optional
from datetime import datetime

# ✅ Campos comunes para creación y lectura (sin IDs ni fechas automáticas)
class TrabajosBase(BaseModel):
    trabajo: str

# ✅ Para CREAR cargo (cliente envía estos campos )
class TrabajosCreate(TrabajosBase):
    pass  # ← Hereda TODO de UserBase

# ✅ Para Update cargo (cliente envía estos campos )
class TrabajosUpdate(BaseModel):
    trabajo_id: str
    trabajo: str

# ✅ Para Update estado (cliente envía estos campos )
class TrabajosUpdateState(BaseModel):
    trabajo_id: str
    flag: bool

class DeleteTrabajosResponse(BaseModel):
    message: str

    class Config:
        from_attributes = True

# ✅ Para devolver
class TrabajosA(TrabajosBase):
    trabajo_id: str
    flag: bool
    created_at: datetime  # importante para la respuesta
    updated_at: datetime  # importante para la respuesta

    class Config:
        from_attributes = True

# ✅ Para devolver respuesta con mensaje + cargo
class TrabajosResponse(BaseModel):
    message: str
    trabajo: TrabajosA

    class Config:
        from_attributes = True