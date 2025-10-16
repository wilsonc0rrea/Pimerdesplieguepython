# backend/schemas.py
from pydantic import BaseModel
from typing import List, Optional
from datetime import datetime

# ✅ Campos comunes para creación y lectura (sin IDs ni fechas automáticas)
class RolesBase(BaseModel):
    rol: str

# ✅ Para CREAR cargo (cliente envía estos campos )
class RolesCreate(RolesBase):
    pass  # ← Hereda TODO de UserBase

# ✅ Para Update cargo (cliente envía estos campos )
class RolesUpdate(BaseModel):
    rol_id: str
    rol: str

# ✅ Para Update estado (cliente envía estos campos )
class RolesUpdateState(BaseModel):
    rol_id: str
    flag: bool

class DeleteRolesResponse(BaseModel):
    message: str

    class Config:
        from_attributes = True

# ✅ Para devolver
class Roles(RolesBase):
    rol_id: str
    flag: bool
    created_at: datetime  # importante para la respuesta
    updated_at: datetime  # importante para la respuesta

    class Config:
        from_attributes = True

class Roleslist(RolesBase):
    rol_id: str

    class Config:
        from_attributes = True

# ✅ Para devolver respuesta con mensaje + cargo
class RolesResponse(BaseModel):
    message: str
    rol: Roles

    class Config:
        from_attributes = True