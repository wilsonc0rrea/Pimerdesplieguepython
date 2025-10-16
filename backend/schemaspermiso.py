# backend/schemas.py
from pydantic import BaseModel
from typing import List, Optional
from datetime import datetime
from decimal import Decimal

# ✅ Campos comunes para creación y lectura (sin IDs ni fechas automáticas)
class PermisosBase(BaseModel):
    concepto: str
    valor: Decimal
    usuario_id: str
    cuentadestino_id: int

# ✅ Para CREAR cargo (cliente envía estos campos )
class PermisosCreate(BaseModel):
    concepto: str
    valor: Decimal
    usuario_id: str
    cuentadestino_id: int

# ✅ Para Update cargo (cliente envía estos campos )
class PermisosUpdate(BaseModel):
    controladorpermiso_id: int
    ver: int
    crear: int
    editar: int
    eliminar: int

# ✅ Para devolver
class Permisos(BaseModel):
    controladorpermiso_id: int
    controlador_id: int
    ver: int
    crear: int
    editar: int
    eliminar: int
    class Config:
        from_attributes = True

class PermisosWCD(BaseModel):
    controladorpermiso_id: int
    ver:int

    class Config:
        from_attributes = True

# ✅ Para devolver respuesta con mensaje + cargo
class PermisosResponse(BaseModel):
    message: str
    permisos: PermisosWCD

    class Config:
        from_attributes = True