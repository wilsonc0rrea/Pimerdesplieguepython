# backend/schemas.py
from pydantic import BaseModel
from typing import List, Optional
from datetime import datetime

# ✅ Campos comunes para creación y lectura (sin IDs ni fechas automáticas)
class CuentasdestinoBase(BaseModel):
    cuenta_destino: str

# ✅ Para devolver
class Cuentasdestino(CuentasdestinoBase):
    cuentadestino_id: int
    flag: bool

    class Config:
        from_attributes = True

class Cdestinolist(CuentasdestinoBase):
    cuentadestino_id: int

    class Config:
        from_attributes = True

# ✅ Para devolver respuesta con mensaje + cargo
class CuentasResponse(BaseModel):
    message: str
    cuentadestino: Cuentasdestino

    class Config:
        from_attributes = True