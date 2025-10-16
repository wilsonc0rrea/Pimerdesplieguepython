# backend/schemas.py
from pydantic import BaseModel
from typing import List, Optional
from datetime import datetime

# ✅ Campos comunes para creación y lectura (sin IDs ni fechas automáticas)
class ClientesBase(BaseModel):
    clientes: str
    identificacion: str
    numero_contacto: str
    pais_id: int

# ✅ Para CREAR cliente (cliente envía estos campos )
class ClientesCreate(ClientesBase):
    pass  # ← Hereda TODO de UserBase

# ✅ Para Update cliente (cliente envía estos campos )
class ClientesUpdate(BaseModel):
    cliente_id: str
    clientes: str
    identificacion: str
    numero_contacto: str
    pais_id: int

# ✅ Para Update estado (cliente envía estos campos )
class ClientesUpdateState(BaseModel):
    cliente_id: str
    flag: bool

class DeleteClienteResponse(BaseModel):
    message: str

    class Config:
        from_attributes = True

# ✅ Para devolver
class Paises(BaseModel):
    pais_id: int
    paises: str

    class Config:
        from_attributes = True

# ✅ Para devolver
class Clientes(BaseModel):
    cliente_id: str
    clientes: str
    identificacion: str
    numero_contacto: str
    pais: Optional[Paises] = None
    flag: bool
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True

class ClientesWCD(BaseModel):
    cliente_id: str
    clientes: str

    class Config:
        from_attributes = True


# ✅ Para devolver respuesta con mensaje + cargo
class ClientesResponse(BaseModel):
    message: str
    cliente: ClientesWCD

    class Config:
        from_attributes = True