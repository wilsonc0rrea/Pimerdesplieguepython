# backend/schemas.py
from pydantic import BaseModel
from typing import List, Optional
from datetime import datetime
from decimal import Decimal

# ✅ Campos comunes para creación y lectura (sin IDs ni fechas automáticas)
class IngresosBase(BaseModel):
    concepto: str
    valor: Decimal
    usuario_id: str
    cuentadestino_id: int

# ✅ Para CREAR cargo (cliente envía estos campos )
class IngresosCreate(BaseModel):
    concepto: str
    valor: Decimal
    usuario_id: str
    cuentadestino_id: int

# ✅ Para Update cargo (cliente envía estos campos )
class IngresosUpdate(BaseModel):
    ingreso_id: str
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

class DeleteIngresosResponse(BaseModel):
    message: str

    class Config:
        from_attributes = True

# ✅ Para devolver
class Ingresos(BaseModel):
    ingreso_id: str
    concepto:str
    valor:Decimal
    cuenta_destino: Optional[Cuentadestino] = None
    usuario:Optional[Usuarios] = None
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True

class IngresosWCD(BaseModel):
    ingreso_id: str
    concepto:str

    class Config:
        from_attributes = True

# ✅ Para devolver respuesta con mensaje + cargo
class IngresosResponse(BaseModel):
    message: str
    ingresos: IngresosWCD

    class Config:
        from_attributes = True