# backend/schemas.py
from pydantic import BaseModel
from typing import List, Optional
from datetime import datetime

# ✅ Campos comunes para creación y lectura (sin IDs ni fechas automáticas)
class CargoBase(BaseModel):
    cargo: str

# ✅ Para CREAR cargo (cliente envía estos campos )
class CargosCreate(CargoBase):
    pass  # ← Hereda TODO de UserBase

# ✅ Para Update cargo (cliente envía estos campos )
class CargosUpdate(BaseModel):
    cargo_id: str
    cargo: str

# ✅ Para Update estado (cliente envía estos campos )
class CargosUpdateState(BaseModel):
    cargo_id: str
    flag: bool

class DeleteCargoResponse(BaseModel):
    message: str

    class Config:
        from_attributes = True

# ✅ Para devolver
class Cargos(CargoBase):
    cargo_id: str
    flag: bool
    created_at: datetime  # importante para la respuesta
    updated_at: datetime  # importante para la respuesta

    class Config:
        from_attributes = True

class Cargoslist(CargoBase):
    cargo_id: str

    class Config:
        from_attributes = True

# ✅ Para devolver respuesta con mensaje + cargo
class CargosResponse(BaseModel):
    message: str
    cargo: Cargos

    class Config:
        from_attributes = True