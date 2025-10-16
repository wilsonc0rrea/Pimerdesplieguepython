# backend/schemas.py
from pydantic import BaseModel, EmailStr  # ✅ ¡Importa EmailStr!
from typing import Optional
from datetime import datetime

# ✅ Campos comunes para creación y lectura (sin IDs ni fechas automáticas)
class UserBase(BaseModel):
    usuario_nombre: str
    usuario_email: EmailStr  # ← ¡Validación de email automática!
    usuario_password: str

# ✅ Para CREAR usuario (cliente envía estos campos )
class UserCreate(UserBase):
    pass  # ← Hereda TODO de UserBase


# ✅ Para devolver usuario desde la BD (sin password)
class User(UserBase):
    usuario_id: str
    usuario_nombre: str
    usuario_email: EmailStr
    usuario_estado: bool
    created_at: datetime

    class Config:
        from_attributes = True


# Para cargar el perfil y editarlo
class Perfil(BaseModel):
    usuario_id: str
    usuario_nombre: str
    usuario_apellido: str
    usuario_telefono: str
    usuario_email: EmailStr
    usuario_password: str

    class Config:
        from_attributes = True

class UserUpdate(BaseModel):
    cargo_id: str
    cargo: str

class PerfilUpdate(BaseModel):
    usuario_id: str
    usuario_nombre: str
    usuario_telefono: Optional[str] = None
    usuario_email: str
    usuario_password: Optional[str] = None


class General(BaseModel):
    usuario_id: str
    usuario_nombre: str
    usuario_telefono: Optional[str] = None
    usuario_email: str
    usuario_password: Optional[str] = None

# ✅ Para JWT
class Token(BaseModel):
    access_token: str
    token_type: str

class LoginIn(BaseModel):
    usuario_email: str
    usuario_password: str

# ✅ Para respuesta de login (usuario + token)
class LoginResponse(BaseModel):
    user: User
    token: Token

class PerfilResponse(BaseModel):
    user: User
