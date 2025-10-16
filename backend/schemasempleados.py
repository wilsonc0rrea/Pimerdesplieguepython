# backend/schemas.py
from pydantic import BaseModel
from typing import List, Optional
from datetime import datetime

# ✅ Campos comunes para creación y lectura (sin IDs ni fechas automáticas)
class EmpleadosBase(BaseModel):
    nombre: str
    direccion: str
    telefonos: str
    email: str
    cargo_id: str
    rol_id: str

# ✅ Para CREAR cliente (cliente envía estos campos )
class EmpleadosCreate(EmpleadosBase):
    pass  # ← Hereda TODO de UserBase

# ✅ Para Update cliente (cliente envía estos campos )
class EmpleadosUpdate(BaseModel):
    empleado_id: str
    nombre: str
    direccion: str
    telefonos: str
    email: str
    cargo_id: str
    rol_id: str

# ✅ Para Update estado (cliente envía estos campos )
class EmpleadosUpdateState(BaseModel):
    empleado_id: str
    flag: bool

class DeleteEmpleadosResponse(BaseModel):
    message: str

    class Config:
        from_attributes = True

# ✅ Para devolver
class Roles(BaseModel):
    rol_id: str
    rol: str

    class Config:
        from_attributes = True

# ✅ Para devolver
class Cargos(BaseModel):
    cargo_id: str
    cargo: str

    class Config:
        from_attributes = True

# ✅ Para devolver
class Empleados(BaseModel):
    empleado_id: str
    nombre: str
    direccion: str
    telefonos: str
    email: str
    rol: Optional[Roles] = None
    cargo: Optional[Cargos] = None
    flag: bool
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True

class EmpleadosWCD(BaseModel):
    empleado_id: str
    nombre: str

    class Config:
        from_attributes = True


# ✅ Para devolver respuesta con mensaje + cargo
class EmpleadosResponse(BaseModel):
    message: str
    empleado: EmpleadosWCD

    class Config:
        from_attributes = True