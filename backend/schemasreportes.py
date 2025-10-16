# backend/schemas.py
from pydantic import BaseModel, field_serializer
from typing import List, Optional
from datetime import datetime,date

# ✅ Campos comunes para creación y lectura (sin IDs ni fechas automáticas)
class ReportesBase(BaseModel):
    cliente_id: str
    seriales: str
    vin: str
    motor: str
    trabajo_id: str
    precio: str
    usuario_id: str
    fecha_servicio: date
    estado_id: int
    observacion: str

# ✅ Para CREAR usuario (cliente envía estos campos )
class ReportesCreate(BaseModel):
    cliente_id: str
    fecha_servicio: date
    seriales: str
    vin: str
    motor: str
    trabajo_id: str
    precio: str
    estado_id: int
    observacion: str
    usuario_id: str

# ✅ Para Update cliente (cliente envía estos campos )
class ReportesUpdate(BaseModel):
    serial_id: str
    fecha_servicio: date
    cliente_id: str
    seriales: str
    vin: str
    motor: str
    trabajo_id: str
    precio: str
    estado_id: int
    observacion: str
    updated_usuario_id: str

class ReportesUpdateCartera(BaseModel):
    serial_id: str
    precio: str
    updated_usuario_id: str

class ReportesUpdateState(BaseModel):
    serial_id: str
    flag: bool


class DeleteReportesResponse(BaseModel):
    message: str

    class Config:
        from_attributes = True

class SerialesReportesResponse(BaseModel):
    serial_id: str
    seriales: Optional[str]= None

    class Config:
        from_attributes = True


# ✅ Para devolver
class Trabajos(BaseModel):
    trabajo_id: str
    trabajo: str

    class Config:
        from_attributes = True

class Empleados(BaseModel):
    empleado_id: str
    nombre: str

    class Config:
        from_attributes = True

class Clientes(BaseModel):
    cliente_id: str
    clientes: str

    class Config:
        from_attributes = True

class Estado_cuentas(BaseModel):
    estado_id: int
    estado: str

    class Config:
        from_attributes = True

class User(BaseModel):
    usuario_id: str
    usuario_nombre: str

    class Config:
        from_attributes = True

# ✅ Para devolver
class Reportes(ReportesBase):
    serial_id: str
    seriales: Optional[str]= None
    vin: Optional[str]= None
    motor: Optional[str] = None
    trabajo: Optional[Trabajos] = None
    precio: Optional[str] = None
    usuario: Optional[User] = None
    flag: bool
    created_at: datetime
    updated_at: datetime
    clientes: Optional[Clientes] = None
    fecha_servicio: date
    estado: Optional[Estado_cuentas] = None
    observacion: Optional[str]= None

    class Config:
        from_attributes = True

class ReportesWCD(BaseModel):
    serial_id: str
    clientes: Optional[Clientes] = None

    class Config:
        from_attributes = True


class ReportesResponse(BaseModel):
    message: str
    reporte: ReportesWCD

    class Config:
        from_attributes = True