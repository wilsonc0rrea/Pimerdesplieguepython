# backend/schemas.py
from pydantic import BaseModel
from typing import List, Optional
from datetime import datetime
from decimal import Decimal

# ✅ Campos comunes para creación y lectura (sin IDs ni fechas automáticas)
class SaldosBase(BaseModel):
      saldo_id: str
      saldo: Decimal
      debe: Decimal
      haber: Decimal
      cuentadestino_id: int
      observacion: str
      created_at: datetime  # importante para la respuesta
      updated_at: datetime  # importante para la respuesta

# ✅ Para CREAR cargo (cliente envía estos campos )
class SaldosCreate(BaseModel):
      saldo: Decimal
      cuentadestino_id: int
      observacion: str
      usuario_id: str

# ✅ Para Update cargo (cliente envía estos campos )
class SaldosUpdate(BaseModel):
      saldo_id: str
      saldo: Decimal
      cuentadestino_id: int
      observacion: str
      usuario_id: str

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

# ✅ Para devolver
class Saldos(BaseModel):
    saldo_id: str
    saldo: Decimal
    debe: Decimal
    haber: Decimal
    cuenta_destino: str
    cuenta_destino: Optional[Cuentadestino] = None
    cuentadestino_id: int
    observacion: str
    usuario_id:str
    usuario:Optional[Usuarios] = None
    created_at: datetime  # importante para la respuesta
    updated_at: datetime  # importante para la respuesta

    class Config:
        from_attributes = True


class SaldosWCD(BaseModel):
    saldo_id: str
    saldo: Decimal

    class Config:
        from_attributes = True

# ✅ Para devolver respuesta con mensaje + cargo
class SaldosResponse(BaseModel):
    message: str
    saldos: SaldosWCD

    class Config:
        from_attributes = True