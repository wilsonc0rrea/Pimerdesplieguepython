# backend/schemas.py
from pydantic import BaseModel
from typing import List, Optional
from datetime import datetime
from decimal import Decimal

# ✅ Campos comunes para creación y lectura (sin IDs ni fechas automáticas)
class CuentasBase(BaseModel):
    cuenta: str

# ✅ Para devolver
class Cuentas(CuentasBase):
    cuenta_id: int
    flag: bool

    class Config:
        from_attributes = True

class Mpagolist(CuentasBase):
    cuenta_id: int

    class Config:
        from_attributes = True

class Clientes(BaseModel):
    cliente_id: str
    clientes: str

    class Config:
        from_attributes = True

class Carteraxcobrar(BaseModel):
    debe: Decimal
    haber: Decimal
    clientes: str
    cliente_id: str
    saldo: Decimal
    class Config:
        from_attributes = True

class CarteraxcobrarWCD(BaseModel):
    cliente_id: str
    class Config:
        from_attributes = True

class CarteraxcobrarCreate(BaseModel):
    cliente_id: str
    debe: Decimal
    haber: Decimal
    usuario_id: str
    clientes: str
    cuenta_id: int
    cuentadestino_id: int

class CarteraxcobrarResponse(BaseModel):
    message: str
    cartera: CarteraxcobrarWCD

    class Config:
        from_attributes = True

# ✅ Para devolver respuesta con mensaje + cargo
class CuentasResponse(BaseModel):
    message: str
    cuenta: Cuentas

    class Config:
        from_attributes = True