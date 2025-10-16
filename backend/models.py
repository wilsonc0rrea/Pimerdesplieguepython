# backend/models.py
from sqlalchemy import Column, String, Boolean, DateTime, Date, func, Integer, ForeignKey, Double, Float
from datetime import datetime,date
from database import Base
from sqlalchemy.orm import relationship
class TimestampMixin:
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow)
    flag = Column(Boolean, default=True)

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
    # ✅ usuario_estado como tinyint(1) → Boolean en Python
    email_verified = Column(Boolean, default=True)
    # ✅ created_at como timestamp
    created_at = Column(DateTime, default=datetime.utcnow)
    # ✅ rol_id como char(36) # FK con roles
    rol_id = Column(String(36), ForeignKey("roles.rol_id"), nullable=False)
    rol = relationship("Roles", back_populates="usuarios")

    reportes = relationship("Reportes", back_populates="usuario")
    saldos = relationship("Saldosiniciales", back_populates="usuario")
    egresos = relationship("Egresos", back_populates="usuario")
    ingresos = relationship("Ingresos", back_populates="usuario")


    def __repr__(self):
        return f"<User {self.usuario_email}>"


class ControladoresPermisos(Base):
    __tablename__ = "controladores_permisos"

    # ✅ tabajo_id como char(36) y PK
    controladorpermiso_id = Column(String(36), primary_key=True, nullable=False)
    # ✅ trabajo como varchar(120)

    ver = Column(Integer, nullable=False)
    crear = Column(Integer, nullable=False)
    editar = Column(Integer, nullable=False)
    eliminar = Column(Integer, nullable=False)
    rol_id = Column(String(36), ForeignKey("roles.rol_id"), nullable=False)
    controlador_id = Column(Integer, ForeignKey("controladores.controlador_id"), nullable=False)
    controlador = relationship("Controladores", back_populates="permisos")
    def __repr__(self):
        return f"<ControladoresPermisos {self.controlador}>"

class Controladores(Base):
    __tablename__ = "controladores"

    # ✅ tabajo_id como char(36) y PK
    controlador_id = Column(Integer, primary_key=True, nullable=False)
    # ✅ trabajo como varchar(120)
    controlador = Column(String(150), nullable=False)
    permisos = relationship("ControladoresPermisos", back_populates="controlador")
    def __repr__(self):
        return f"<Controladores {self.controlador}>"

class Cargos(Base,TimestampMixin):
    __tablename__ = "cargos"

    # ✅ tabajo_id como char(36) y PK
    cargo_id = Column(String(36), primary_key=True, nullable=False)
    # ✅ trabajo como varchar(120)
    cargo = Column(String(120), nullable=False)

    # Relación inversa con Empleados
    empleados = relationship("Empleados", back_populates="cargo")

    def __repr__(self):
        return f"<Cargos {self.cargo}>"

class Carteraxcobrar(Base,TimestampMixin):
    __tablename__ = "carteraxcobrar"

    cartera_id = Column(Integer, primary_key=True, nullable=False)
    usuario_id = Column(String(36), nullable=False)
    # ✅ trabajo como varchar(120)
    debe = Column(Double, nullable=False)
    haber = Column(Double, nullable=False)
    cuenta_id = Column(Integer, nullable=False)
    cuentadestino_id = Column(Integer, nullable=False)
    # Relación inversa con Empleados
    cliente_id = Column(String(36), ForeignKey("clientes.cliente_id"), nullable=False)
    clientes = relationship("Clientes", back_populates="cartera")
    serial_id = Column(String(36), nullable=False)
    def __repr__(self):
        return f"<Carteraxcobrar {self.debe}>"

class Saldosiniciales(Base):
    __tablename__ = "saldosiniciales"

    saldo_id = Column(String(36), primary_key=True, nullable=False)
    saldo = Column(Double, nullable=False)
    debe = Column(Double, nullable=False)
    haber = Column(Double, nullable=False)
    observacion = Column(String(120), nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow)

    # Relación inversa
    cuentadestino_id = Column(Integer, ForeignKey("cuentadestino.cuentadestino_id"), nullable=False)
    cuenta_destino = relationship("Cuentadestino", back_populates="saldo")

    usuario_id = Column(String(36), ForeignKey("usuarios.usuario_id"), nullable=False)
    usuario = relationship("User", back_populates="saldos")
    egreso_id = Column(String(36), nullable=True)
    def __repr__(self):
        return f"<Saldosiniciales {self.debe}>"

class Egresos(Base):
    __tablename__ = "egresos"

    egreso_id = Column(String(36), primary_key=True, nullable=False)
    concepto = Column(String(200), nullable=False)
    valor = Column(Double, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow)

    cuentadestino_id = Column(Integer, ForeignKey("cuentadestino.cuentadestino_id"), nullable=False)
    cuenta_destino = relationship("Cuentadestino", back_populates="egresos")

    usuario_id = Column(String(36), ForeignKey("usuarios.usuario_id"), nullable=False)
    usuario = relationship("User", back_populates="egresos")  # ✅ SINGULAR

    def __repr__(self):
        return f"<Egresos {self.concepto}>"

class Ingresos(Base):
    __tablename__ = "ingresos"

    ingreso_id = Column(String(36), primary_key=True, nullable=False)
    concepto = Column(String(200), nullable=False)
    valor = Column(Double, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow)

    cuentadestino_id = Column(Integer, ForeignKey("cuentadestino.cuentadestino_id"), nullable=False)
    cuenta_destino = relationship("Cuentadestino", back_populates="ingresos")

    usuario_id = Column(String(36), ForeignKey("usuarios.usuario_id"), nullable=False)
    usuario = relationship("User", back_populates="ingresos")  # ✅ SINGULAR

    def __repr__(self):
        return f"<Ingresos {self.concepto}>"

class Cuentabancaria(Base):
    __tablename__ = "cuentabancaria"

    cuenta_id = Column(Integer, primary_key=True, nullable=False)
    cuenta = Column(String(120), nullable=False)

    def __repr__(self):
        return f"<Cuentabancaria {self.cuenta}>"

class Cuentadestino(Base):
    __tablename__ = "cuentadestino"

    cuentadestino_id = Column(Integer, primary_key=True, nullable=False)
    # ✅ trabajo como varchar(120)
    cuenta_destino = Column(String(120), nullable=False)

    saldo = relationship("Saldosiniciales", back_populates="cuenta_destino")
    egresos = relationship("Egresos", back_populates="cuenta_destino")
    ingresos = relationship("Ingresos", back_populates="cuenta_destino")

    def __repr__(self):
        return f"<Cuentadestino {self.cuenta_destino}>"

class Trabajos(Base,TimestampMixin):
    __tablename__ = "tipotrabajo"

    # ✅ tabajo_id como char(36) y PK
    trabajo_id = Column(String(36), primary_key=True, nullable=False)
    # ✅ trabajo como varchar(120)
    trabajo = Column(String(120), nullable=False)

    # Relación inversa con Reportes
    reportes = relationship("Reportes", back_populates="trabajo")

    def __repr__(self):
        return f"<Trabajos {self.trabajo}>"


class Paises(Base):
    __tablename__ = "paises"

    # ✅ pais_id como char(36) y PK
    pais_id = Column(String(36), primary_key=True, nullable=False)
    # ✅ paises como varchar(120)
    paises = Column(String(200), nullable=False)
    # ✅ iso como varchar(3)
    iso = Column(String(3))


    def __repr__(self):
        return f"<Paises {self.paises}>"

class Estadocuentas(Base,TimestampMixin):
    __tablename__ = "estadocuenta"

    # ✅ pais_id como char(11) y PK
    estado_id = Column(Integer, primary_key=True, nullable=False)
    # ✅ paises como varchar(120)
    estado = Column(String(60), nullable=False)

    # Relación inversa: un empleado tiene MUCHOS reportes
    reportes = relationship("Reportes", back_populates="estado")  # ✅ PLURAL

    def __repr__(self):
        return f"<Estadocuenta {self.estado}>"


class Clientes(Base,TimestampMixin):
    __tablename__ = "clientes"

    # ✅ cliente_id como char(36) y PK
    cliente_id = Column(String(36), primary_key=True, nullable=False)
    # ✅ cliente como varchar(120)
    clientes = Column(String(120), nullable=False)
    # ✅ idientificacion como varchar(120)
    identificacion = Column(String(30), nullable=False)
    # ✅ numero de contacto como string(30)
    numero_contacto = Column(String(30), nullable=False)
    # ✅ Solo estas dos líneas para la relación
    pais_id = Column(Integer, ForeignKey('paises.pais_id'), nullable=True)
    pais = relationship("Paises", backref="Clientes")

    # Relación inversa con Reportes
    reportes = relationship("Reportes", back_populates="clientes")

    # Relación inversa con Cartera
    cartera = relationship("Carteraxcobrar", back_populates="clientes")

    def __repr__(self):
        return f"<Clientes {self.clientes}>"

class Roles(Base,TimestampMixin):
    __tablename__ = "roles"

    # ✅ rol_id como char(36) y PK
    rol_id = Column(String(36), primary_key=True, nullable=False)
    # ✅ cliente como varchar(100)
    rol = Column(String(100), nullable=False)

    # Relación inversa con Empleados
    empleados = relationship("Empleados", back_populates="rol")
    # Relación inversa con Usuarios
    usuarios = relationship("User", back_populates="rol")

    def __repr__(self):
        return f"<Roles {self.rol}>"

class Empleados(Base,TimestampMixin):
    __tablename__ = "empleados"

    # ✅ empleado_id como char(36) y PK
    empleado_id = Column(String(36), primary_key=True, nullable=False)
    # ✅ empleados como varchar(120)
    nombre = Column(String(120), nullable=False)
    # ✅ direccion como varchar(120)
    direccion = Column(String(120), nullable=False)
    # ✅ telefonos como varchar(36)
    telefonos = Column(String(36), nullable=False)
    # ✅ email como varchar(120)
    email = Column(String(120), nullable=False)
    # FK con cargos
    cargo_id = Column(String(36), ForeignKey("cargos.cargo_id"), nullable=False)
    cargo = relationship("Cargos", back_populates="empleados")
    # FK con roles
    rol_id = Column(String(36), ForeignKey("roles.rol_id"), nullable=False)
    rol = relationship("Roles", back_populates="empleados")

    # Relación inversa: un empleado tiene MUCHOS reportes
    #reportes = relationship("Reportes", back_populates="empleado")  # ✅ PLURAL

    def __repr__(self):
        return f"<Empleados {self.nombre}>"

class Reportes(Base,TimestampMixin):
    __tablename__ = "reportes"

    # ✅ empleado_id como char(36) y PK
    serial_id = Column(String(36), primary_key=True, nullable=False)
    # ✅ seriales como varchar(50)
    seriales = Column(String(50), nullable=False)
    # ✅ vin como varchar(50)
    vin = Column(String(50), nullable=False)
    # ✅ motor como varchar(50)
    motor = Column(String(50), nullable=False)
    # FK con trabajos
    trabajo_id = Column(String(36), ForeignKey("tipotrabajo.trabajo_id"), nullable=False)
    trabajo = relationship("Trabajos", back_populates="reportes")
    # ✅ precio como double(15)
    precio = Column(String(20), nullable=True)
    usuario_id = Column(String(36), ForeignKey("usuarios.usuario_id"), nullable=False)
    usuario = relationship("User", back_populates="reportes")  # ✅ SINGULAR
    # FK con clientes
    cliente_id = Column(String(36), ForeignKey("clientes.cliente_id"), nullable=False)
    clientes = relationship("Clientes", back_populates="reportes")
    # ✅ fecha como date
    fecha_servicio = Column(Date)
    # FK con estadocuenta
    estado_id = Column(Integer, ForeignKey("estadocuenta.estado_id"), nullable=False)
    estado = relationship("Estadocuentas", back_populates="reportes")
    # ✅ observacion
    observacion = Column(String(120), nullable=True)
    # ✅ usuario updated services
    updated_usuario_id = Column(String(36), nullable=True)

    def __repr__(self):
        return f"<Reportes {self.seriales}>"

class TokenBlacklist(Base):
    __tablename__ = "token_blacklist"

    usuario_id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    token = Column(String, unique=True, index=True, nullable=False)
    invalidated_at = Column(DateTime(timezone=True), server_default=func.now())
    # ✅ usuario_estado como tinyint(1) → Boolean en Python
    usuario_estado = Column(Boolean, default=True)