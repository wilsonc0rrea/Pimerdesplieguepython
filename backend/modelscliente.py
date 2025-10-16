# backend/models.py
from sqlalchemy import Column, String, Boolean, DateTime, func
from datetime import datetime
from database import Base

class User(Base):
    __tablename__ = "usuarios"

    # ✅ usuario_id como char(36) y PK
    usuario_id = Column(String(36), primary_key=True, nullable=False)
    # ✅ usuario_nombre como varchar(200)
    usuario_nombre = Column(String(200), nullable=False)
    # ✅ usuario_apellido como varchar(200)
    usuario_apellido = Column(String(200), nullable=False)
    # ✅ usuario_telefono como varchar(100)
    usuario_telefono = Column(String(100), nullable=True)
    # ✅ usuario_email como varchar(100) y único
    usuario_email = Column(String(100), unique=True, nullable=False)
    # ✅ usuario_password como varchar(60) para bcrypt
    usuario_password = Column(String(255), nullable=False)
    # ✅ usuario_unico como char(36)
    usuario_unico = Column(String(36), unique=True, nullable=True)
    # ✅ usuario_estado como tinyint(1) → Boolean en Python
    usuario_estado = Column(Boolean, default=True)
    # ✅ created_at como timestamp
    created_at = Column(DateTime, default=datetime.utcnow)
    def __repr__(self):
        return f"<User {self.usuario_email}>"

class TokenBlacklist(Base):
    __tablename__ = "token_blacklist"

    usuario_id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    token = Column(String, unique=True, index=True, nullable=False)
    invalidated_at = Column(DateTime(timezone=True), server_default=func.now())
    # ✅ usuario_estado como tinyint(1) → Boolean en Python
    usuario_estado = Column(Boolean, default=True)