# backend/schemas.py
from pydantic import BaseModel
from typing import List, Optional
from datetime import datetime
from decimal import Decimal

# ✅ Campos comunes para creación y lectura (sin IDs ni fechas automáticas)
class EgresosBase(BaseModel):
    concepto: str
    valor: Decimal
    usuario_id: str
    cuentadestino_id: int

# ✅ Para CREAR cargo (cliente envía estos campos )
class EgresosCreate(BaseModel):
    concepto: str
    valor: Decimal
    usuario_id: str
    cuentadestino_id: int

# ✅ Para Update cargo (cliente envía estos campos )
class EgresosUpdate(BaseModel):
    egreso_id: str
    concepto: str
    valor: Decimal
    usuario_id: str
    cuentadestino_id: int

class Usuarios(BaseModel):
    usuario_id: str
    usuario_nombre: str

    class Config:
        from_attributes = True

class Cuentadestino(BaseModel):
    cuentadestino_id: int
    cuenta_destino: str

    class Config:
        from_attributes = True

class DeleteEgresosResponse(BaseModel):
    message: str

    class Config:
        from_attributes = True

# ✅ Para devolver
class Egresos(BaseModel):
    egreso_id: str
    concepto:str
    valor:Decimal
    cuenta_destino: Optional[Cuentadestino] = None
    usuario:Optional[Usuarios] = None
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True

class EgresosWCD(BaseModel):
    egreso_id: str
    concepto:str

    class Config:
        from_attributes = True

# ✅ Para devolver respuesta con mensaje + cargo
class EgresosResponse(BaseModel):
    message: str
    egresos: EgresosWCD

    class Config:
        from_attributes = True