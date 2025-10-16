# -------------------------------------------------------------------
# 📅 Importamos 'datetime' para trabajar con fechas y horas.
# Útil para registrar timestamps de creación/actualización de registros,
# validar rangos de fechas, o formatear fechas en respuestas.
# -------------------------------------------------------------------
from datetime import datetime,timedelta
import pytz
# -------------------------------------------------------------------
# 🧩 Importamos tipos de anotación para mejorar la legibilidad del código,
# la validación en tiempo de desarrollo y la documentación automática de FastAPI.
# - 'List[T]' → indica que una variable es una lista de elementos de tipo T.
# - 'Optional[T]' → indica que una variable puede ser T o None (útil para campos opcionales).
# -------------------------------------------------------------------
from typing import List, Optional
# -------------------------------------------------------------------
# 🔢 Importamos 'uuid' para generar identificadores únicos universales.
# Ideal para usar como IDs en lugar de enteros autoincrementales:
# - Más seguros (evitan ataques por enumeración).
# - Escalables en microservicios.
# - Compatibles con APIs públicas.
# Ejemplo: user_id = str(uuid.uuid4())
# -------------------------------------------------------------------
import uuid
# -------------------------------------------------------------------
# 🚀 Importamos componentes esenciales de FastAPI:
# - 'FastAPI': Clase principal para crear la aplicación.
# - 'Depends': Para inyección de dependencias (ej: conexión a base de datos, autenticación).
# - 'HTTPException': Para lanzar errores HTTP controlados (404, 400, 500, etc).
# - 'status': Constantes con códigos HTTP (mejor que usar números mágicos como 404).
# -------------------------------------------------------------------
from fastapi import FastAPI, Depends, HTTPException, status, Response,Cookie
from fastapi.responses import JSONResponse,RedirectResponse
# -------------------------------------------------------------------
# 🌐 Importamos el middleware CORS para permitir que tu API sea consumida
# desde frontends en dominios/puertos diferentes (ej: localhost:3000 → localhost:8000).
# Sin esto, los navegadores bloquearán las peticiones por política de seguridad.
# Configurable para permitir ciertos orígenes, métodos y headers.
# -------------------------------------------------------------------
from fastapi.middleware.cors import CORSMiddleware
# -------------------------------------------------------------------
# 📦 Importamos 'BaseModel' de Pydantic para definir modelos de datos.
# Se usan para:
# - Validar automáticamente el cuerpo de las peticiones entrantes.
# - Definir la estructura de las respuestas.
# - Generar documentación automática en /docs (Swagger UI).
# Ejemplo: class UserCreate(BaseModel): name: str; email: str
# -------------------------------------------------------------------
from pydantic import BaseModel
# -------------------------------------------------------------------
# 🗃️ Importamos 'Session' de SQLAlchemy ORM.
# Representa una sesión de base de datos: es el objeto que usas para hacer
# queries, inserts, updates, deletes, etc.
# Se inyecta típicamente en las rutas mediante Depends(get_db).
# -------------------------------------------------------------------
from sqlalchemy.orm import Session, joinedload
# -------------------------------------------------------------------
# 🛠️ Importamos 'text' de SQLAlchemy para ejecutar SQL crudo de forma segura.
# Útil cuando necesitas consultas complejas que el ORM no cubre bien.
# ¡NUNCA concatenes strings SQL! Usa 'text()' con parámetros para evitar inyecciones.
# Ejemplo: db.execute(text("SELECT * FROM users WHERE age > :age"), {"age": 18})
# -------------------------------------------------------------------
from sqlalchemy import text,func,and_,extract
# -------------------------------------------------------------------
# 💡 ANTES DE USAR VARIABLES DE ENTORNO: Cargamos el archivo .env
# 'load_dotenv()' lee el archivo .env y carga sus variables en os.environ.
# Esto permite mantener configuraciones sensibles (contraseñas, claves, URLs)
# fuera del código fuente, facilitando el despliegue en múltiples entornos.
# DEBE llamarse ANTES de cualquier os.getenv().
# -------------------------------------------------------------------
from dotenv import load_dotenv
# -------------------------------------------------------------------
# 🖥️ Importamos el módulo 'os' para interactuar con el sistema operativo.
# Principalmente usado para:
# - Leer variables de entorno con os.getenv("CLAVE", "valor_por_defecto").
# - Manipular rutas de archivos, directorios, etc.
# Esencial para leer configuraciones del sistema de forma segura y portable.
# -------------------------------------------------------------------
import os
# -------------------------------------------------------------------
# ✅ RECOMENDACIÓN: Llama a load_dotenv() justo después de los imports.
# Así garantizas que las variables estén disponibles antes de usarlas.
# -------------------------------------------------------------------
load_dotenv()  # <-- ¡No olvides llamarlo!

# Configuración desde .env
# -------------------------------------------------------------------
# 🌐 CORS_ORIGINS: Define los orígenes (dominios) permitidos para hacer peticiones a tu API.
# - Por defecto: "http://localhost:5173" (típico puerto de Vite/Vue.js en desarrollo).
# - Se espera una cadena separada por comas (ej: "http://localhost:3000,https://miapp.com").
# - Se convierte en una LISTA de strings para usarla en el middleware CORS de FastAPI.
# - ¡IMPORTANTE! En producción, NUNCA uses ["*"] a menos que sea una API pública sin auth.
# -------------------------------------------------------------------
#CORS_ORIGINS = os.getenv("CORS_ORIGINS", "http://localhost:5173").split(",")
CORS_ORIGINS = os.getenv("CORS_ORIGINS")

# -------------------------------------------------------------------
# 🔑 SECRET_KEY: Clave secreta usada para firmar tokens (JWT), sesiones, cookies, etc.
# - DEBE ser única, larga y aleatoria (ej: generada con `openssl rand -hex 32`).
# - NO debe estar en código fuente ni en repositorios públicos.
# - Si no se define en .env, la aplicación debería fallar (no hay valor por defecto).
# - Ejemplo de uso: firmar tokens JWT con `python-jose` o `passlib`.
# -------------------------------------------------------------------
SECRET_KEY = os.getenv("SECRET_KEY")
ALGORITHM = os.getenv("ALGORITHM")
ACCESS_TOKEN_EXPIRE_MINUTES= os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES")
# -------------------------------------------------------------------
# 🗃️ DATABASE_URL: Cadena de conexión a la base de datos.
# - Formato típico: "postgresql://user:password@host:port/database"
# - También soporta SQLite: "sqlite:///./nombre.db"
# - SQLAlchemy lo usa para crear el motor de conexión.
# - Si no está definida, la app NO podrá conectarse a la base de datos → debe fallar.
# - ¡NUNCA commitear credenciales reales! Usa .env o secretos de despliegue (Docker, Railway, Render, etc).
# -------------------------------------------------------------------
DATABASE_URL = os.getenv("DATABASE_URL")

# Importaciones de tu app (¡después de cargar .env!)
# -------------------------------------------------------------------
# 🗃️ Importamos componentes esenciales de la capa de base de datos:
# - 'engine': Motor de SQLAlchemy que gestiona la conexión con la base de datos.
#             Se usa para crear tablas (Base.metadata.create_all(engine)) o migraciones.
# - 'SessionLocal': Fábrica de sesiones. Cada petición HTTP crea una sesión nueva para interactuar con la DB.
# - 'Base': Clase base declarativa de SQLAlchemy. Todos los modelos heredan de ella.
# - 'get_db': Dependencia de FastAPI que inyecta una sesión de DB en las rutas.
#             Se usa con: db: Session = Depends(get_db)
# -------------------------------------------------------------------
from database import engine, SessionLocal, Base, get_db
# -------------------------------------------------------------------
# 🧱 Importamos los 'models' (modelos de SQLAlchemy).
# - Representan las tablas de la base de datos como clases de Python.
# - Definen columnas, relaciones, constraints, etc.
# - Ejemplo: class User(Base): __tablename__ = "users"; id = Column(String, primary_key=True)
# - Se usan en las consultas ORM: db.query(User).filter(...).first()
# - ¡Importante! Deben importarse ANTES de crear las tablas con Base.metadata.create_all(engine)
# -------------------------------------------------------------------
import models
# -------------------------------------------------------------------
# 📦 Importamos los 'schemas' (modelos de Pydantic).
# - Definen la estructura de los datos que entran (request) y salen (response) de la API.
# - Se usan para validar y serializar datos automáticamente.
# - Ejemplo: class UserCreate(BaseModel): name: str; email: EmailStr
# - Diferencia clave: 'models' → DB | 'schemas' → API
# -------------------------------------------------------------------
import schemas
import schemasreportes
import schemascargos
import schemastrabajos
import schemasclientes
import schemasroles
import schemasempleados
import schemasestadocuenta
import schemascarteraxcobrar
import schemascuentadestino
import schemassaldos
import schemasegresos
import schemasingresos
import schemaspermiso
# -------------------------------------------------------------------
# 🔐 Importamos el módulo 'security' (seguridad de la aplicación).
# - Contiene funciones relacionadas con autenticación y autorización.
# - Ejemplos típicos:
#     - verify_password(plain, hashed) → verifica contraseñas.
#     - get_password_hash(password) → hashea contraseñas.
#     - create_access_token(data) → genera tokens JWT.
#     - get_current_user(token) → decodifica token y obtiene usuario (para rutas protegidas).
# - Esencial para endpoints de login, registro y rutas autenticadas.
# -------------------------------------------------------------------
import security
import jwt
from jwt.exceptions import ExpiredSignatureError, InvalidTokenError
# 📨 smtplib: Módulo estándar de Python para enviar correos usando protocolo SMTP
# → Nos permite conectarnos a servidores de correo (Gmail, Outlook, etc.) y enviar mensajes.
import smtplib
# 🔐 ssl: Módulo para crear conexiones seguras (TLS/SSL)
# → Lo usamos para cifrar la conexión con el servidor SMTP (evita que alguien intercepte tu contraseña).
import ssl
# 📄 MIMEText: Clase para crear partes de un mensaje de correo con contenido de texto (HTML o plain text)
# → Lo usamos para adjuntar el cuerpo HTML del correo.
from email.mime.text import MIMEText
# 📦 MIMEMultipart: Clase para crear un mensaje de correo con múltiples partes (ej: texto + HTML + adjuntos)
# → ¡ES CLAVE! Permite estructurar el correo correctamente (con asunto, remitente, destinatario, cuerpo HTML, etc.).
from email.mime.multipart import MIMEMultipart  # 👈 ¡ESTA ES LA CLAVE!

import logging
# Crea un logger global
logger = logging.getLogger("uvicorn.error")
#----- Configurar zona horaria
colombia_tz = pytz.timezone('America/Bogota')

# --- Configuración de la app ---
app = FastAPI(
    title="Reportes diarios...",
    description="✨ API profesional con validación",
    version="1.0.0"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        origin.strip()
        for origin in os.getenv("CORS_ORIGINS", "http://localhost:5173").split(",")],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# helper to set cookie
def set_refresh_cookie(response: Response, token_value: str, expires_days: int):
    """
    Envía el refresh token en una cookie HttpOnly + Secure + SameSite=Strict.
    Se recomienda usar Secure=True en producción (HTTPS).
    """
    response.set_cookie(
        key="refresh_token",        # el navegador no permite leerla con JS (document.cookie), protegiendo contra XSS.
        value=token_value,
        httponly=True,              # No accesible desde JS (mitiga XSS)
        secure=False,               # ⚠️ True en producción (HTTPS)
        samesite="strict",         # Evita CSRF; usa 'lax' si tu front está en otro dominio
        max_age=expires_days * 24 * 60 * 60,
        path="/api/refresh"       # Opcional: limita la cookie a esta ruta
    )



# --- Modelos auxiliares ---

MENU_DATA = [

    {
       "label": "Salir",
       "icon": "pi pi-sign-out",
       "command": "logout",
       "modulo": 'Salir'
    },
    {
        "label": "Inicio",
        "icon": "pi pi-home",
        "to": "/dashboard",
        "modulo": 'Inicio'
    },
    {
         "label": "Finanzas",
         "icon": "pi pi-cog",
         "modulo": 'Finanzas',
         "items": [
             {"label": "Cartera", "icon": "pi pi-check-circle", "to": "/finanzas/carteraxcobrar","modulo": 'Cartera'},
             {"label": "Saldos", "icon": "pi pi-check-circle", "to": "/finanzas/saldos","modulo": 'Saldos'},
             {"label": "Egresos", "icon": "pi pi-check-circle", "to": "/finanzas/egresos","modulo": 'Egresos'},
             {"label": "Ingresos", "icon": "pi pi-check-circle", "to": "/finanzas/ingresos","modulo": 'Ingresos'},
         ]
    },
    {
        "label": "Informes",
        "icon": "pi pi-cog",
        "modulo": 'Informes',
        "items": [
            {
                "label": "Reportes",
                "icon": "pi pi-check-circle",
                "modulo": 'CReportes',
                "items": [
                    {"label": "Crear Reportes", "icon": "pi pi-check-circle", "to": "/config/reportes","modulo": 'Reportes'},
                    {"label": "Listado", "icon": "pi pi-check-circle", "to": "/config/listadoreporte","modulo": 'Listado'},

                ]
            },
            {
                "label": "Estadística",
                "icon": "pi pi-check-circle",
                "modulo": 'Estadistica',
                "items": [
                    {"label": "servicios", "icon": "pi pi-check-circle", "to": "/config/estadisticaservicio","modulo": 'Estadistica servicios'},
                    {"label": "trabajos", "icon": "pi pi-check-circle", "to": "/config/estadisticatrabajos","modulo": 'Estadistica trabajos'}
                ]
            },
        ]

    },
    {
        "label": "Configuración",
        "icon": "pi pi-cog",
        "modulo": 'Configuración',
        "items": [
            {
               "label": "Maestros",
               "icon": "pi pi-plus",
               "modulo": 'Maestros',
               "items": [
                   {"label": "Cargos", "icon": "pi pi-check-circle", "to": "/config/cargos","modulo": 'Cargos'},
                   {"label": "Tipos", "icon": "pi pi-check-circle", "to": "/config/ttrabajos","modulo": 'Tipos'},
                   {"label": "Clientes", "icon": "pi pi-check-circle", "to": "/config/clientes","modulo": 'Clientes'},
                   {"label": "Roles", "icon": "pi pi-check-circle", "to": "/config/roles","modulo": 'Roles'},
                   #{"label": "Empleados", "icon": "pi pi-check-circle", "to": "/config/empleados"},
                   {"label": "Perfil", "icon": "pi pi-check-circle", "to": "/config/perfil","modulo": 'Perfil'},
                   {"label": "Permisos", "icon": "pi pi-plus", "to": "/config/permisos","modulo": 'Permisos'},
               ]
            },

        ]
    }
]

# --- Rutas ---
@app.get("/api/menu")
async def get_menu():
    return MENU_DATA

@app.get("api/validatokens")
async def get_me(db: Session = Depends(get_db), email: str = Depends(security.get_current_user_from_cookie)):
    user = db.query(models.User).filter(models.User.usuario_email == email).first()
    if not user:
        raise HTTPException(status_code=404, detail="Usuario no encontrado")

    return {
        "usuario_id": user.usuario_id,
        "usuario_nombre": user.usuario_nombre,
        "usuario_email": user.usuario_email,
        "rol": user.rol.rol if user.rol else None
    }


@app.post("/api/salir")
async def logout(response: Response):
    try:
        response.set_cookie(
            key="access_token",
            value="",
            httponly=True,
            samesite="Strict",
            secure=False,
            max_age=0,  # 👈 Esto elimina la cookie
            path="/"
        )
        return {"message": "Sesión cerrada"}
    except Exception as e:
            print("❌ Error :", str(e))  # ← ¡Esto es clave!
            raise HTTPException(status_code=401, detail="Token inválido")

@app.post("/api/login", response_model=schemas.Token)
async def login(user: schemas.LoginIn, db: Session = Depends(get_db)):

        # 1. Buscar usuario por email
        db_user = db.query(models.User).filter(models.User.usuario_email == user.usuario_email).first()

        if not db_user:
            raise HTTPException(status_code=404, detail="Usuario no encontrado")

        # 2. Verificar contraseña
        if not security.verify_password(user.usuario_password, db_user.usuario_password):
            raise HTTPException(status_code=401, detail="Contraseña inconrrecta")

        # 3. Crear tokens
        access_token = security.create_access_token(data={"sub": db_user.usuario_id})

        permisos = db.query(models.ControladoresPermisos).options(
                 joinedload(models.ControladoresPermisos.controlador)
                 ).filter(models.ControladoresPermisos.rol_id == db_user.rol_id).all()

        controlador_data = [
            {
                "modulo": p.controlador.controlador,
                "ver": p.ver,
                "crear": p.crear,
                "editar": p.editar,
                "eliminar": p.eliminar
            }
            for p in permisos
        ] if permisos else []

        # 4. Respuesta con cookie y datos de usuario
        response = JSONResponse(
            content={
                "usuario_id": db_user.usuario_id,
                "usuario_nombre": db_user.usuario_nombre,
                "usuario_email": db_user.usuario_email,
                "usuario_estado": db_user.usuario_estado,
                "rol": {
                    "rol_id": db_user.rol.rol_id,
                    "rol": db_user.rol.rol
                } if db_user.rol else None,
                "controlador": controlador_data,
                "token": {"access_token": access_token,"token_type": "bearer"}
            }
        )
        # 5. Guardamos cookie segura
        # secure=False,   ponlo True en producción (HTTPS)
        # max_age=3600    # 1 hora
        response.set_cookie(
            key="access_token",
            value=access_token,
            httponly=True, # 🔒 Inaccesible desde JS
            samesite="Strict",
            secure=False, # Cambia a True en producción (HTTPS)
            max_age=3600, # 1 hora
            path="/"  # ✅ ¡Esto es clave!
        )
        #set_refresh_cookie(response, refresh_token, expires_days=7)
        return response

def get_current_user_from_cookie(access_token: Optional[str] = Cookie(None), db: Session = Depends(get_db)):
    if not access_token:
        raise HTTPException(status_code=401, detail="No autenticado")

    if not SECRET_KEY or not ALGORITHM:
       raise HTTPException(status_code=500, detail="Error interno: variables de entorno no configuradas")

    try:
        payload = jwt.decode(access_token, SECRET_KEY, algorithms=[ALGORITHM])  # tu función de decodificar JWT
        usuario_id: str = payload.get("sub")
        if usuario_id is None:
            raise HTTPException(status_code=401, detail="Token inválido")
    except Exception as e:
        print("❌ Error al decodificar:", str(e))  # ← ¡Esto es clave!
        raise HTTPException(status_code=401, detail="Token inválido")

    user = db.query(models.User).filter(models.User.usuario_id == usuario_id).first()
    if user is None:
        raise HTTPException(status_code=401, detail="Usuario no encontrado")
    return user

@app.get("/api/me")
async def read_users_me(current_user: models.User = Depends(get_current_user_from_cookie), db: Session = Depends(get_db)):
    # Cargar permisos del usuario
    permisos = db.query(models.ControladoresPermisos).options(
        joinedload(models.ControladoresPermisos.controlador)
    ).filter(models.ControladoresPermisos.rol_id == current_user.rol_id).all()

    controlador_data = [
        {
            "modulo": p.controlador.controlador,
            "ver": p.ver,
            "crear": p.crear,
            "editar": p.editar,
            "eliminar": p.eliminar
        }
        for p in permisos
    ] if permisos else []

    return {
        "usuario_id": current_user.usuario_id,
        "usuario_nombre": current_user.usuario_nombre,
        "usuario_email": current_user.usuario_email,
        "usuario_estado": current_user.usuario_estado,
        "rol": {
            "rol_id": current_user.rol.rol_id,
            "rol": current_user.rol.rol
        } if current_user.rol else None,
        "controlador": controlador_data
    }

#-------------------------- Seccion de crear ---------------------------------
@app.post("/api/register", response_model=schemas.User)
async def register(user: schemas.UserCreate, db: Session = Depends(get_db)):

        # Verificar si el email ya existe
        db_user = db.query(models.User).filter(models.User.usuario_email == user.usuario_email).first()
        if db_user:
            raise HTTPException(status_code=400, detail="Email ya registrado")

        # Intentar hashear la contraseña
        try:
           hashed_password = security.get_password_hash(user.usuario_password)
        except Exception as e:
           raise HTTPException(status_code=500,
                        detail=f"Error al procesar la contraseña: {str(e)}"
                    )

        # Crear nuevo usuario
        new_user = models.User(
            usuario_id=str(uuid.uuid4()),
            usuario_nombre=user.usuario_nombre,
            usuario_apellido="",  # ❗ ¡Agrega esto! Tu modelo lo requiere
            usuario_telefono="",
            usuario_email=user.usuario_email,  # Asumiendo que en UserCreate se llama "email"
            usuario_password=hashed_password,
            usuario_unico=str(uuid.uuid4()),
            usuario_estado=0,
            created_at=datetime.now(colombia_tz)  # ¡Corregido! Era solo "datetime"
        )


        db.add(new_user)
        db.commit()
        db.refresh(new_user)
        # ✅ Generar link de verificación
        verification_link = f"{os.getenv('FRONTEND_URL')}/api/verify-email?token={new_user.usuario_unico}"
        # ✅ Enviar correo
        if not send_verification_email(new_user.usuario_email, verification_link,new_user.usuario_nombre,):
            # Opcional: puedes decidir si fallar el registro o no
            # Aquí solo logueamos, pero el usuario se crea igual
            print("⚠️ No se pudo enviar el correo de verificación")
            raise HTTPException(status_code=400, detail="No se pudo enviar el correo de verificación")

        return new_user  # Devuelve el modelo SQLAlchemy, Pydantic lo serializará

@app.post("/api/creacargos", response_model=schemascargos.CargosResponse)
async def crear_cargo(cargo: schemascargos.CargosCreate, db: Session = Depends(get_db)):
    try:
        # Verificar si ya existe
        db_cargo = db.query(models.Cargos).filter(models.Cargos.cargo == cargo.cargo).first()
        if db_cargo:
            raise HTTPException(status_code=400, detail="Cargo registrado anteriormente")

        # Crear cargo
        new_cargo = models.Cargos(
            cargo_id=str(uuid.uuid4()),
            cargo=cargo.cargo,
            flag=True,
            created_at=datetime.now(colombia_tz),
            updated_at=datetime.now(colombia_tz)  # ¡Corregido! Era solo "datetime"
        )
        db.add(new_cargo)
        db.commit()
        db.refresh(new_cargo)

        return {
            "message": f"Cargo '{new_cargo.cargo}' creado correctamente",
            "cargo": new_cargo
        }

    except HTTPException:
        raise  # Re-lanza el error para que FastAPI lo maneje
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=f"Error en el servidor: {str(e)}")

@app.post("/api/creacarteraxcobrar", response_model=schemascarteraxcobrar.CarteraxcobrarResponse)
async def crear_carteraxcobrar(cartera: schemascarteraxcobrar.CarteraxcobrarCreate, db: Session = Depends(get_db)):
    try:

        # Crear cartera
        new_cartera = models.Carteraxcobrar(
            cliente_id=cartera.cliente_id,
            usuario_id=cartera.usuario_id,
            debe=0,
            haber=cartera.haber,
            cuenta_id=cartera.cuenta_id,
            cuentadestino_id=cartera.cuentadestino_id,
            created_at=datetime.now(colombia_tz),
            updated_at=datetime.now(colombia_tz)  # ¡Corregido! Era solo "datetime"
        )

        new_saldo = models.Saldosiniciales(
            saldo_id=str(uuid.uuid4()),
            saldo=0,
            debe=0,
            haber=cartera.haber,
            cuentadestino_id=cartera.cuentadestino_id,
            observacion='Servicio',
            usuario_id=cartera.usuario_id,
            created_at=datetime.now(colombia_tz),
            updated_at=datetime.now(colombia_tz)
        )

        db.add(new_saldo)
        db.add(new_cartera)
        db.commit()
        db.refresh(new_cartera)

        return {
            "message": f"Cartera generada correctamente",
            "cartera": new_cartera
        }

    except HTTPException:
        raise  # Re-lanza el error para que FastAPI lo maneje
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=f"Error en el servidor: {str(e)}")


@app.post("/api/crearoles", response_model=schemasroles.RolesResponse)
async def crear_roles(roles: schemasroles.RolesCreate, db: Session = Depends(get_db)):
    try:
        # Verificar si ya existe
        db_rol = db.query(models.Roles).filter(models.Roles.rol == roles.rol).first()
        if db_rol:
            raise HTTPException(status_code=400, detail="Rol registrado anteriormente")

        # Crear roles
        new_rol = models.Roles(
            rol_id=str(uuid.uuid4()),
            rol=roles.rol,
            flag=True,
            created_at=datetime.now(colombia_tz),
            updated_at=datetime.now(colombia_tz)  # ¡Corregido! Era solo "datetime"
        )
        db.add(new_rol)
        db.commit()
        db.refresh(new_rol)

        return {
            "message": f"Rol '{new_rol.rol}' creado correctamente",
            "rol": new_rol
        }

    except HTTPException:
        raise  # Re-lanza el error para que FastAPI lo maneje
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=f"Error en el servidor: {str(e)}")

@app.post("/api/creaegresos", response_model=schemasegresos.EgresosResponse)
async def crear_egresos(egreso: schemasegresos.EgresosCreate, db: Session = Depends(get_db)):
    try:
        # Crear
        new_egreso = models.Egresos(
            egreso_id=str(uuid.uuid4()),
            concepto=egreso.concepto,
            valor=egreso.valor,
            usuario_id=egreso.usuario_id,
            cuentadestino_id=egreso.cuentadestino_id,
            created_at=datetime.now(colombia_tz),
            updated_at=datetime.now(colombia_tz)  # ¡Corregido! Era solo "datetime"
        )
        db.add(new_egreso)
        db.commit()
        db.refresh(new_egreso)
        egresosID = new_egreso.egreso_id

        new_saldos = models.Saldosiniciales(
            saldo_id=str(uuid.uuid4()),
            saldo=0,
            debe=egreso.valor,
            haber=0,
            cuentadestino_id=egreso.cuentadestino_id,
            egreso_id=egresosID,
            observacion=egreso.concepto,
            usuario_id=egreso.usuario_id,
            created_at=datetime.now(colombia_tz),
            updated_at=datetime.now(colombia_tz)
        )
        db.add(new_saldos)
        db.commit()
        db.refresh(new_saldos)

        return {
            "message": f"Egreso '{new_egreso.concepto}' creado correctamente",
            "egresos": new_egreso
        }

    except HTTPException:
        raise  # Re-lanza el error para que FastAPI lo maneje
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=f"Error en el servidor: {str(e)}")

@app.post("/api/creaingresos", response_model=schemasingresos.IngresosResponse)
async def crear_ingresos(ingreso: schemasingresos.IngresosCreate, db: Session = Depends(get_db)):
    try:
        # Crear
        new_ingreso = models.Ingresos(
            ingreso_id=str(uuid.uuid4()),
            concepto=ingreso.concepto,
            valor=ingreso.valor,
            usuario_id=ingreso.usuario_id,
            cuentadestino_id=ingreso.cuentadestino_id,
            created_at=datetime.now(colombia_tz),
            updated_at=datetime.now(colombia_tz)  # ¡Corregido! Era solo "datetime"
        )
        db.add(new_ingreso)
        db.commit()
        db.refresh(new_ingreso)
        ingresosID = new_ingreso.ingreso_id

        new_saldos = models.Saldosiniciales(
            saldo_id=str(uuid.uuid4()),
            saldo=0,
            debe=0,
            haber=ingreso.valor,
            cuentadestino_id=ingreso.cuentadestino_id,
            egreso_id=ingresosID,
            observacion=ingreso.concepto,
            usuario_id=ingreso.usuario_id,
            created_at=datetime.now(colombia_tz),
            updated_at=datetime.now(colombia_tz)
        )
        db.add(new_saldos)
        db.commit()
        db.refresh(new_saldos)

        return {
            "message": f"Ingreso '{new_ingreso.concepto}' creado correctamente",
            "ingresos": new_ingreso
        }

    except HTTPException:
        raise  # Re-lanza el error para que FastAPI lo maneje
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=f"Error en el servidor: {str(e)}")


@app.post("/api/creaingresos", response_model=schemasingresos.IngresosResponse)
async def crear_ingresos(ingreso: schemasingresos.IngresosCreate, db: Session = Depends(get_db)):
    try:
        # Crear
        new_ingreso = models.Ingresos(
            ingreso_id=str(uuid.uuid4()),
            concepto=egreso.concepto,
            valor=egreso.valor,
            usuario_id=egreso.usuario_id,
            cuentadestino_id=egreso.cuentadestino_id,
            created_at=datetime.now(colombia_tz),
            updated_at=datetime.now(colombia_tz)  # ¡Corregido! Era solo "datetime"
        )
        db.add(new_ingreso)
        db.commit()
        db.refresh(new_ingreso)
        ingresosID = new_ingreso.ingreso_id

        new_saldos = models.Saldosiniciales(
            saldo_id=str(uuid.uuid4()),
            saldo=0,
            debe=0,
            haber=ingreso.valor,
            cuentadestino_id=ingreso.cuentadestino_id,
            egreso_id=ingresosID,
            observacion=ingreso.concepto,
            usuario_id=ingreso.usuario_id,
            created_at=datetime.now(colombia_tz),
            updated_at=datetime.now(colombia_tz)
        )
        db.add(new_saldos)
        db.commit()
        db.refresh(new_saldos)

        return {
            "message": f"Ingreso '{new_ingreso.concepto}' creado correctamente",
            "ingresos": new_ingreso
        }

    except HTTPException:
        raise  # Re-lanza el error para que FastAPI lo maneje
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=f"Error en el servidor: {str(e)}")


@app.post("/api/crearsaldos", response_model=schemassaldos.SaldosResponse)
async def crear_saldos(saldo: schemassaldos.SaldosCreate, db: Session = Depends(get_db)):
    try:
        # Crear

        new_saldos = models.Saldosiniciales(
            saldo_id=str(uuid.uuid4()),
            saldo=saldo.saldo,
            debe=0,
            haber=0,
            cuentadestino_id=saldo.cuentadestino_id,
            observacion=saldo.observacion,
            usuario_id=saldo.usuario_id,
            created_at=datetime.now(colombia_tz),
            updated_at=datetime.now(colombia_tz)
        )
        db.add(new_saldos)
        db.commit()
        db.refresh(new_saldos)

        return {
            "message": f"Saldo creado correctamente",
            "saldos": new_saldos
        }

    except HTTPException:
        raise  # Re-lanza el error para que FastAPI lo maneje
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=f"Error en el servidor: {str(e)}")


@app.post("/api/creatipotrabajos", response_model=schemastrabajos.TrabajosResponse)
async def crear_cargo(trabajo: schemastrabajos.TrabajosCreate, db: Session = Depends(get_db)):
    try:
        # Verificar si ya existe
        db_trabajo = db.query(models.Trabajos).filter(models.Trabajos.trabajo == trabajo.trabajo).first()
        if db_trabajo:
            raise HTTPException(status_code=400, detail="Tipo de trabajo registrado anteriormente")

        # Crear cargo
        new_tipotrabajo = models.Trabajos(
            trabajo_id=str(uuid.uuid4()),
            trabajo=trabajo.trabajo,
            flag=True,
            created_at=datetime.now(colombia_tz),
            updated_at=datetime.now(colombia_tz)  # ¡Corregido! Era solo "datetime"
        )
        db.add(new_tipotrabajo)
        db.commit()
        db.refresh(new_tipotrabajo)

        return {
            "message": f"Cargo '{new_tipotrabajo.trabajo}' creado correctamente",
            "trabajo": new_tipotrabajo
        }

    except HTTPException:
        raise  # Re-lanza el error para que FastAPI lo maneje
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=f"Error en el servidor: {str(e)}")


@app.post("/api/creaclientes", response_model=schemasclientes.ClientesResponse)
async def crear_cliente(cliente: schemasclientes.ClientesCreate, db: Session = Depends(get_db)):
    try:
        # Verificar si ya existe
        db_cliente = db.query(models.Clientes).filter(models.Clientes.identificacion == cliente.identificacion).first()
        if db_cliente:
            raise HTTPException(status_code=400, detail="Cliente registrado anteriormente")
        # Crear cliente
        new_cliente = models.Clientes(
            cliente_id=str(uuid.uuid4()),
            clientes=cliente.clientes,
            identificacion=cliente.identificacion,
            numero_contacto=cliente.numero_contacto,
            pais_id=cliente.pais_id,
            flag=True,
            created_at=datetime.now(colombia_tz),
            updated_at=datetime.now(colombia_tz)  # ¡Corregido! Era solo "datetime"
        )
        db.add(new_cliente)
        db.commit()
        db.refresh(new_cliente)
        return {
            "message": f"Clientes '{new_cliente.clientes}' creado correctamente",
            "cliente": new_cliente
        }

    except HTTPException:
        raise  # Re-lanza el error para que FastAPI lo maneje
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=f"Error en el servidor: {str(e)}")

@app.post("/api/creareportes", response_model=schemasreportes.ReportesResponse)
async def crear_cliente(reporte: schemasreportes.ReportesCreate, db: Session = Depends(get_db)):
    try:
        # Crear cliente
        new_reporte = models.Reportes(
            serial_id=str(uuid.uuid4()),
            cliente_id=reporte.cliente_id,
            seriales=reporte.seriales,
            vin=reporte.vin,
            motor=reporte.motor,
            trabajo_id=reporte.trabajo_id,
            precio=reporte.precio,
            flag=True,
            created_at=datetime.now(colombia_tz),
            updated_at=datetime.now(colombia_tz),  # ¡Corregido! Era solo "datetime"
            fecha_servicio=reporte.fecha_servicio,
            estado_id=reporte.estado_id,
            observacion=reporte.observacion,
            usuario_id=reporte.usuario_id
        )
        db.add(new_reporte)
        db.commit()
        db.refresh(new_reporte)
        return {
            "message": f"Reporte actualizado correctamente",
            "reporte": new_reporte
        }

    except HTTPException:
        raise  # Re-lanza el error para que FastAPI lo maneje
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=f"Error en el servidor: {str(e)}")



@app.post("/api/creaempleados", response_model=schemasempleados.EmpleadosResponse)
async def crear_empleados(empleado: schemasempleados.EmpleadosCreate, db: Session = Depends(get_db)):
    try:
        # Verificar si ya existe
        db_empleado = db.query(models.Empleados).filter(models.Empleados.email == empleado.email).first()
        if db_empleado:
            raise HTTPException(status_code=400, detail="Empleado registrado anteriormente, por favor verificar email")
        # Crear cliente
        new_empleado = models.Empleados(
            empleado_id=str(uuid.uuid4()),
            nombre=empleado.nombre,
            direccion=empleado.direccion,
            telefonos=empleado.telefonos,
            email=empleado.email,
            rol_id=empleado.rol_id,
            cargo_id=empleado.cargo_id,
            flag=True,
            created_at=datetime.now(colombia_tz),
            updated_at=datetime.now(colombia_tz)  # ¡Corregido! Era solo "datetime"
        )
        db.add(new_empleado)
        db.commit()
        db.refresh(new_empleado)
        return {
            "message": f"Clientes '{new_empleado.nombre}' creado correctamente",
            "empleado": new_empleado
        }

    except HTTPException:
        raise  # Re-lanza el error para que FastAPI lo maneje
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=f"Error en el servidor: {str(e)}")

@app.post("/api/crearusuario", response_model=schemas.User)
async def register(user: schemas.UserCreate, db: Session = Depends(get_db)):

        # Verificar si el email ya existe
        db_user = db.query(models.User).filter(models.User.usuario_email == user.usuario_email).first()
        if db_user:
            raise HTTPException(status_code=400, detail="Email ya registrado")

        # Intentar hashear la contraseña
        try:
           hashed_password = security.get_password_hash(user.usuario_password)
        except Exception as e:
           raise HTTPException(status_code=500,
                        detail=f"Error al procesar la contraseña: {str(e)}"
                    )


        # Crear nuevo usuario
        new_user = models.User(
            usuario_id=str(uuid.uuid4()),
            usuario_nombre=user.usuario_nombre,
            usuario_apellido="",  # ❗ ¡Agrega esto! Tu modelo lo requiere
            usuario_telefono="",
            usuario_email=user.usuario_email,  # Asumiendo que en UserCreate se llama "email"
            usuario_password=hashed_password,
            usuario_unico=str(uuid.uuid4()),
            usuario_estado=1,
            created_at=datetime.now(colombia_tz),  # ¡Corregido! Era solo "datetime"
            updated_at=datetime.now(colombia_tz)  # ¡Corregido! Era solo "datetime"
        )


        db.add(new_user)
        db.commit()
        db.refresh(new_user)
        return new_user  # Devuelve el modelo SQLAlchemy, Pydantic lo serializará

#-------------------------- Seccion de actualizar ---------------------------------
@app.put("/api/updatecargos", response_model=schemascargos.CargosResponse)
async def update_cargo(cargo: schemascargos.CargosUpdate, db: Session = Depends(get_db)):
    try:
        # Buscar el cargo por ID
        db_cargo = db.query(models.Cargos).filter(models.Cargos.cargo_id == cargo.cargo_id).first()

        # ❗ Si NO existe → error 404
        if not db_cargo:
            raise HTTPException(status_code=404, detail="Cargo no encontrado con el ID proporcionado")

        # ✅ Si SÍ existe → actualizamos
        db_cargo.cargo = cargo.cargo  # actualiza el nombre
        db_cargo.updated_at = datetime.now(colombia_tz)  # marca la fecha de actualización

        db.commit()
        db.refresh(db_cargo)

        return {
            "message": f"Cargo '{db_cargo.cargo}' actualizado correctamente",
            "cargo": db_cargo
        }

    except HTTPException:
        raise
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=f"Error en el servidor: {str(e)}")

@app.put("/api/updatepermisos", response_model=schemaspermiso.PermisosResponse)
async def update_permisos(permiso: schemaspermiso.PermisosUpdate, db: Session = Depends(get_db)):
    try:
        # Buscar el cargo por ID
        db_permiso = db.query(models.ControladoresPermisos).filter(models.ControladoresPermisos.controladorpermiso_id == permiso.controladorpermiso_id).first()

        # ❗ Si NO existe → error 404
        if not db_permiso:
            raise HTTPException(status_code=404, detail="Controlador no encontrado con el ID proporcionado")

        # ✅ Si SÍ existe → actualizamos
        db_permiso.ver = permiso.ver
        db_permiso.crear = permiso.crear
        db_permiso.editar = permiso.editar
        db_permiso.eliminar = permiso.eliminar
        db.commit()
        db.refresh(db_permiso)
        return {
            "message": f"Módulo actualizado correctamente",
            "permisos": db_permiso
        }
    except HTTPException:
        raise
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=f"Error en el servidor: {str(e)}")


@app.put("/api/updatetipotrabajo", response_model=schemastrabajos.TrabajosResponse)
async def update_trabajo(trabajo: schemastrabajos.TrabajosUpdate, db: Session = Depends(get_db)):
    try:
        # Buscar el cargo por ID
        db_trabajo = db.query(models.Trabajos).filter(models.Trabajos.trabajo_id == trabajo.trabajo_id).first()

        # ❗ Si NO existe → error 404
        if not db_trabajo:
            raise HTTPException(status_code=404, detail="Tipo de trabajo no encontrado con el ID proporcionado")

        # ✅ Si SÍ existe → actualizamos
        db_trabajo.trabajo = trabajo.trabajo  # actualiza el nombre
        db_trabajo.updated_at = datetime.now(colombia_tz)  # marca la fecha de actualización

        db.commit()
        db.refresh(db_trabajo)

        return {
            "message": f"Cargo '{db_trabajo.trabajo}' actualizado correctamente",
            "trabajo": db_trabajo
        }

    except HTTPException:
        raise
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=f"Error en el servidor: {str(e)}")

@app.put("/api/updateroles", response_model=schemasroles.RolesResponse)
async def update_roles(roles: schemasroles.RolesUpdate, db: Session = Depends(get_db)):
    try:
        # Buscar el cargo por ID
        db_rol = db.query(models.Roles).filter(models.Roles.rol_id == roles.rol_id).first()

        # ❗ Si NO existe → error 404
        if not db_rol:
            raise HTTPException(status_code=404, detail="Tipo de rol no encontrado con el ID proporcionado")

        # ✅ Si SÍ existe → actualizamos
        db_rol.rol = roles.rol  # actualiza el nombre
        db_rol.updated_at = datetime.now(colombia_tz)  # marca la fecha de actualización

        db.commit()
        db.refresh(db_rol)

        return {
            "message": f"Cargo '{db_rol.rol}' actualizado correctamente",
            "rol": db_rol
        }

    except HTTPException:
        raise
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=f"Error en el servidor: {str(e)}")

@app.put("/api/updateegresos", response_model=schemasegresos.EgresosResponse)
async def update_roles(egresos: schemasegresos.EgresosUpdate, db: Session = Depends(get_db)):
    try:
        # Buscar el cargo por ID
        db_egreso = db.query(models.Egresos).filter(models.Egresos.egreso_id == egresos.egreso_id).first()

        # ❗ Si NO existe → error 404
        if not db_egreso:
            raise HTTPException(status_code=404, detail="Egreso no encontrado con el ID proporcionado")

        # ✅ Si SÍ existe → actualizamos
        db_egreso.concepto = egresos.concepto
        db_egreso.cuentadestino_id = egresos.cuentadestino_id
        db_egreso.valor = egresos.valor
        db_egreso.usuario_id = egresos.usuario_id
        db_egreso.updated_at = datetime.now(colombia_tz)

        db.commit()
        db.refresh(db_egreso)

        db_saldos = db.query(models.Saldosiniciales).filter(models.Saldosiniciales.egreso_id == egresos.egreso_id).first()

        # ❗ Si NO existe → error 404
        if not db_saldos:
           raise HTTPException(status_code=404, detail="No se encontró saldosiniciales con el ID proporcionado")

        db_saldos.debe=egresos.valor,
        db_saldos.cuentadestino_id=egresos.cuentadestino_id,
        db_saldos.egreso_id=egresos.egreso_id,
        db_saldos.observacion=egresos.concepto,
        db_saldos.usuario_id=egresos.usuario_id,
        db_saldos.updated_at=datetime.now(colombia_tz)

        db.commit()
        db.refresh(db_saldos)

        return {
            "message": f"Egreso '{db_egreso.concepto}' actualizado correctamente",
            "egresos": db_egreso
        }

    except HTTPException:
        raise
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=f"Error en el servidor: {str(e)}")

@app.put("/api/updateingresos", response_model=schemasingresos.IngresosResponse)
async def update_roles(ingresos: schemasingresos.IngresosUpdate, db: Session = Depends(get_db)):
    try:
        # Buscar el cargo por ID
        db_ingreso = db.query(models.Ingresos).filter(models.Ingresos.ingreso_id == ingresos.ingreso_id).first()

        # ❗ Si NO existe → error 404
        if not db_ingreso:
            raise HTTPException(status_code=404, detail="Ingreso no encontrado con el ID proporcionado")

        # ✅ Si SÍ existe → actualizamos
        db_ingreso.concepto = ingresos.concepto
        db_ingreso.cuentadestino_id = ingresos.cuentadestino_id
        db_ingreso.valor = ingresos.valor
        db_ingreso.usuario_id = ingresos.usuario_id
        db_ingreso.updated_at = datetime.now(colombia_tz)

        db.commit()
        db.refresh(db_ingreso)

        db_saldos = db.query(models.Saldosiniciales).filter(models.Saldosiniciales.egreso_id == ingresos.ingreso_id).first()

        # ❗ Si NO existe → error 404
        if not db_saldos:
           raise HTTPException(status_code=404, detail="No se encontró saldosiniciales con el ID proporcionado")

        db_saldos.haber=ingresos.valor,
        db_saldos.cuentadestino_id=ingresos.cuentadestino_id,
        db_saldos.egreso_id=ingresos.ingreso_id,
        db_saldos.observacion=ingresos.concepto,
        db_saldos.usuario_id=ingresos.usuario_id,
        db_saldos.updated_at=datetime.now(colombia_tz)

        db.commit()
        db.refresh(db_saldos)

        return {
            "message": f"Ingreso '{db_ingreso.concepto}' actualizado correctamente",
            "ingresos": db_ingreso
        }

    except HTTPException:
        raise
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=f"Error en el servidor: {str(e)}")


@app.put("/api/updatesaldoinicial", response_model=schemassaldos.SaldosResponse)
async def update_roles(saldo: schemassaldos.SaldosUpdate, db: Session = Depends(get_db)):
    try:
        # Buscar el cargo por ID
        db_saldo = db.query(models.Saldosiniciales).filter(models.Saldosiniciales.saldo_id == saldo.saldo_id).first()

        # ❗ Si NO existe → error 404
        if not db_saldo:
            raise HTTPException(status_code=404, detail="Tipo de saldoinicial no encontrado con el ID proporcionado")

        # ✅ Si SÍ existe → actualizamos
        db_saldo.saldo = saldo.saldo
        db_saldo.cuentadestino_id = saldo.cuentadestino_id
        db_saldo.observacion = saldo.observacion
        db_saldo.usuario_id = saldo.usuario_id
        db_saldo.updated_at = datetime.now(colombia_tz)

        db.commit()
        db.refresh(db_saldo)

        return {
            "message": f"Saldoinicial '{db_saldo.observacion}' actualizado correctamente",
            "saldos": db_saldo
        }

    except HTTPException:
        raise
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=f"Error en el servidor: {str(e)}")


@app.put("/api/updateclientes", response_model=schemasclientes.ClientesResponse)
async def update_cliente(cliente: schemasclientes.ClientesUpdate, db: Session = Depends(get_db)):
    try:
        # Buscar el cliente por ID
        db_cliente = db.query(models.Clientes).filter(models.Clientes.cliente_id == cliente.cliente_id).first()

        # ❗ Si NO existe → error 404
        if not db_cliente:
            raise HTTPException(status_code=404, detail="Cliente no encontrado con el ID proporcionado")

        # ✅ Si SÍ existe → actualizamos
        db_cliente.clientes = cliente.clientes  # actualiza el nombre
        db_cliente.identificacion = cliente.identificacion  # actualiza el nombre
        db_cliente.numero_contacto = cliente.numero_contacto  # actualiza el nombre
        db_cliente.pais_id = cliente.pais_id  # actualiza el nombre
        db_cliente.updated_at = datetime.now(colombia_tz)  # marca la fecha de actualización

        db.commit()
        db.refresh(db_cliente)

        return {
            "message": f"Cliente '{db_cliente.clientes}' actualizado correctamente",
            "cliente": db_cliente
        }

    except HTTPException:
        raise
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=f"Error en el servidor: {str(e)}")

@app.put("/api/updatereportes", response_model=schemasreportes.ReportesResponse)
async def update_reportes(reporte: schemasreportes.ReportesUpdate, db: Session = Depends(get_db)):
    try:
        # Buscar el cliente por ID
        db_reporte = db.query(models.Reportes).filter(models.Reportes.serial_id == reporte.serial_id).first()

        # ❗ Si NO existe → error 404
        if not db_reporte:
            raise HTTPException(status_code=404, detail="Cliente no encontrado con el ID proporcionado")

        nombre_empleado = db_reporte.clientes.clientes
        serial = db_reporte.seriales
        # ✅ Si SÍ existe → actualizamos
        db_reporte.fecha_servicio = reporte.fecha_servicio  # actualiza el nombre
        db_reporte.cliente_id = reporte.cliente_id  # actualiza el nombre
        db_reporte.seriales = reporte.seriales  # actualiza el nombre
        db_reporte.vin = reporte.vin  # actualiza el nombre
        db_reporte.motor = reporte.motor  # actualiza el nombre
        db_reporte.trabajo_id = reporte.trabajo_id  # actualiza el nombre
        db_reporte.precio = reporte.precio  # actualiza el nombre
        db_reporte.empleado_id = reporte.empleado_id  # actualiza el nombre
        db_reporte.updated_at = datetime.now(colombia_tz)  # marca la fecha de actualización
        db_reporte.updated_usuario_id = reporte.updated_usuario_id

        db.commit()
        db.refresh(db_reporte)

        return {
            "message": f"Reporte {nombre_empleado} con serial {serial} actualizado correctamente",
            "reporte": db_reporte
        }

    except HTTPException:
        raise
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=f"Error en el servidor: {str(e)}")

@app.put("/api/updateperfil", response_model=schemas.PerfilResponse)
async def update_perfiles(usuario: schemas.PerfilUpdate, db: Session = Depends(get_db)):
    try:
        print(f"❌ Error enviando correo a {usuario}")

        # Buscar por ID
        db_usuario = db.query(models.User).filter(models.User.usuario_id == usuario.usuario_id).first()

        # ✅ Si SÍ existe → actualizamos
        db_usuario.usuario_nombre = usuario.usuario_nombre
        db_usuario.usuario_telefono = usuario.usuario_telefono
        db_usuario.usuario_email = usuario.usuario_email

        # ✅ Solo actualizar contraseña si se proporciona
        if usuario.usuario_password:
            db_usuario.usuario_password = security.get_password_hash(usuario.usuario_password)

        # ❗ Si NO existe → error 404
        if not db_usuario:
            raise HTTPException(status_code=404, detail="Perfil no encontrado con el ID proporcionado")



        db.commit()
        db.refresh(db_usuario)

        return {
            "message": f"Usuario actualizado correctamente",
            "user": db_usuario
        }

    except HTTPException:
        raise
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=f"Error en el servidor: {str(e)}")


@app.put("/api/updatereporteserviciosxcobrar", response_model=schemasreportes.ReportesResponse)
async def update_reportes(reporte: schemasreportes.ReportesUpdateCartera, db: Session = Depends(get_db)):
    try:
        # Buscar el cliente por ID
        db_reporte = db.query(models.Reportes).filter(models.Reportes.serial_id == reporte.serial_id).first()

        # ❗ Si NO existe → error 404
        if not db_reporte:
            raise HTTPException(status_code=404, detail="Servicio no encontrado con el ID proporcionado")

        nombre_empleado = db_reporte.clientes.clientes
        serial = db_reporte.seriales
        # ✅ Si SÍ existe → actualizamos

        db_reporte.precio = reporte.precio  # actualiza el nombre
        db_reporte.updated_at = datetime.now(colombia_tz)  # marca la fecha de actualización
        db_reporte.updated_usuario_id = reporte.updated_usuario_id

        db.commit()
        db.refresh(db_reporte)

        db_cartera = db.query(models.Carteraxcobrar).filter(models.Carteraxcobrar.serial_id == reporte.serial_id).first()
        if not db_cartera:
            raise HTTPException(status_code=404, detail="Servicio no encontrado con el ID proporcionado, para actualizar cartera")
        db_cartera.debe = reporte.precio  # actualiza el nombre
        db_cartera.updated_at = datetime.now(colombia_tz)  # marca la fecha de actualización
        db_cartera.usuario_id = reporte.updated_usuario_id
        db.commit()
        db.refresh(db_cartera)

        return {
            "message": f"Servicio actualizado correctamente",
            "reporte": db_reporte
        }

    except HTTPException:
        raise
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=f"Error en el servidor: {str(e)}")


@app.put("/api/updateempleados", response_model=schemasempleados.EmpleadosResponse)
async def update_cliente(empleado: schemasempleados.EmpleadosUpdate, db: Session = Depends(get_db)):
    try:
        # Buscar el cliente por ID
        db_empleado = db.query(models.Empleados).filter(models.Empleados.empleado_id == empleado.empleado_id).first()

        # ❗ Si NO existe → error 404
        if not db_empleado:
            raise HTTPException(status_code=404, detail="Empleado no encontrado con el ID proporcionado")

        # ✅ Si SÍ existe → actualizamos
        db_empleado.nombre = empleado.nombre
        db_empleado.direccion = empleado.direccion
        db_empleado.telefonos = empleado.telefonos
        db_empleado.email = empleado.email
        db_empleado.cargo_id = empleado.cargo_id
        db_empleado.rol_id = empleado.rol_id
        db_empleado.updated_at = datetime.now(colombia_tz)  # marca la fecha de actualización

        db.commit()
        db.refresh(db_empleado)

        return {
            "message": f"Empleado '{db_empleado.nombre}' actualizado correctamente",
            "empleado": db_empleado
        }

    except HTTPException:
        raise
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=f"Error en el servidor: {str(e)}")

@app.put("/api/updatecargostate", response_model=schemascargos.CargosResponse)
async def update_cargo(cargo: schemascargos.CargosUpdateState, db: Session = Depends(get_db)):
    try:
        # Buscar el cargo por ID
        db_cargo = db.query(models.Cargos).filter(models.Cargos.cargo_id == cargo.cargo_id).first()

        # ❗ Si NO existe → error 404
        if not db_cargo:
            raise HTTPException(status_code=404, detail="Cargo no encontrado con el ID proporcionado")

        # ✅ Si SÍ existe → actualizamos
        db_cargo.flag = cargo.flag
        db_cargo.updated_at = datetime.now(colombia_tz)  # marca la fecha de actualización

        db.commit()
        db.refresh(db_cargo)

        return {
            "message": f"Cargo '{db_cargo.cargo}' actualizado correctamente",
            "cargo": db_cargo
        }

    except HTTPException:
        raise
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=f"Error en el servidor: {str(e)}")

@app.put("/api/updatetrabajostate", response_model=schemastrabajos.TrabajosResponse)
async def update_trabajo(trabajo: schemastrabajos.TrabajosUpdateState, db: Session = Depends(get_db)):
    try:
        # Buscar el cargo por ID
        db_trabajo = db.query(models.Trabajos).filter(models.Trabajos.trabajo_id == trabajo.trabajo_id).first()

        # ❗ Si NO existe → error 404
        if not db_trabajo:
            raise HTTPException(status_code=404, detail="Tipo de trabajo no encontrado con el ID proporcionado")

        # ✅ Si SÍ existe → actualizamos
        db_trabajo.flag = trabajo.flag
        db_trabajo.updated_at = datetime.now(colombia_tz)  # marca la fecha de actualización

        db.commit()
        db.refresh(db_trabajo)

        return {
            "message": f"Cargo '{db_trabajo.trabajo}' actualizado correctamente",
            "trabajo": db_trabajo
        }

    except HTTPException:
        raise
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=f"Error en el servidor: {str(e)}")


@app.put("/api/updateclientestate", response_model=schemasclientes.ClientesResponse)
async def update_cliente(cliente: schemasclientes.ClientesUpdateState, db: Session = Depends(get_db)):
    try:
        # Buscar el cargo por ID
        db_cliente = db.query(models.Clientes).filter(models.Clientes.cliente_id == cliente.cliente_id).first()

        # ❗ Si NO existe → error 404
        if not db_cliente:
            raise HTTPException(status_code=404, detail="Cliente no encontrado con el ID proporcionado")
        # ✅ Si SÍ existe → actualizamos
        db_cliente.flag = cliente.flag
        db_cliente.updated_at = datetime.now(colombia_tz)  # marca la fecha de actualización
        db.commit()
        db.refresh(db_cliente)
        return {
            "message": f"Cliente '{db_cliente.clientes}' actualizado correctamente",
            "cliente": db_cliente
        }

    except HTTPException:
        raise
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=f"Error en el servidor: {str(e)}")

@app.put("/api/updatereportestate", response_model=schemasreportes.ReportesResponse)
async def update_reporte(reporte: schemasreportes.ReportesUpdateState, db: Session = Depends(get_db)):
    try:
        # Buscar el cargo por ID
        db_reporte = db.query(models.Reportes).filter(models.Reportes.serial_id == reporte.serial_id).first()

        # ❗ Si NO existe → error 404
        if not db_reporte:
            raise HTTPException(status_code=404, detail="Cliente no encontrado con el ID proporcionado")
        # ✅ Si SÍ existe → actualizamos
        db_reporte.flag = reporte.flag
        db_reporte.updated_at = datetime.now(colombia_tz)  # marca la fecha de actualización
        db.commit()
        db.refresh(db_reporte)
        return {
            "message": f"Reporte '{db_reporte.clientes.clientes}' actualizado correctamente",
            "reporte": db_reporte
        }

    except HTTPException:
        raise
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=f"Error en el servidor: {str(e)}")


@app.put("/api/updaterolstate", response_model=schemasroles.RolesResponse)
async def update_rol(roles: schemasroles.RolesUpdateState, db: Session = Depends(get_db)):
    try:
        # Buscar el rol por ID
        db_rol = db.query(models.Roles).filter(models.Roles.rol_id == roles.rol_id).first()

        # ❗ Si NO existe → error 404
        if not db_rol:
            raise HTTPException(status_code=404, detail="Rol no encontrado con el ID proporcionado")

        # ✅ Si SÍ existe → actualizamos
        db_rol.flag = roles.flag
        db_rol.updated_at = datetime.now(colombia_tz)  # marca la fecha de actualización

        db.commit()
        db.refresh(db_rol)

        return {
            "message": f"Rol '{db_rol.rol}' actualizado correctamente",
            "rol": db_rol
        }

    except HTTPException:
        raise
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=f"Error en el servidor: {str(e)}")


@app.put("/api/updateempleadostate", response_model=schemasempleados.EmpleadosResponse)
async def update_rol(empleado: schemasempleados.EmpleadosUpdateState, db: Session = Depends(get_db)):
    try:
        # Buscar el rol por ID
        db_empleado = db.query(models.Empleados).filter(models.Empleados.empleado_id == empleado.empleado_id).first()

        # ❗ Si NO existe → error 404
        if not db_empleado:
            raise HTTPException(status_code=404, detail="Rol no encontrado con el ID proporcionado")

        # ✅ Si SÍ existe → actualizamos
        db_empleado.flag = empleado.flag
        db_empleado.updated_at = datetime.now(colombia_tz)  # marca la fecha de actualización

        db.commit()
        db.refresh(db_empleado)

        return {
            "message": f"Empleado '{db_empleado.nombre}' actualizado correctamente",
            "empleado": db_empleado
        }

    except HTTPException:
        raise
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=f"Error en el servidor: {str(e)}")


#-------------------------- Seccion de eliminar ---------------------------------
@app.put("/api/deletecargos/{cargo_id}", response_model=schemascargos.DeleteCargoResponse)
async def delete_cargo(cargo_id: str, db: Session = Depends(get_db)):
    try:
        # Buscar el cargo por ID
        db_cargo = db.query(models.Cargos).filter(models.Cargos.cargo_id == cargo_id).first()
        # ❗ Si NO existe → error 404
        if not db_cargo:
            raise HTTPException(status_code=404, detail="Cargo no encontrado")

        nombre_cargo = db_cargo.cargo
        # Eliminar físicamente
        db.delete(db_cargo)
        db.commit()

        return {
            "message": f"Cargo {nombre_cargo} eliminado correctamente",
        }

    except HTTPException:
        raise
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=f"Error en el servidor: {str(e)}")

@app.put("/api/deletetrabajos/{trabajo_id}", response_model=schemastrabajos.DeleteTrabajosResponse)
async def delete_trabajo(trabajo_id: str, db: Session = Depends(get_db)):
    try:
        # Buscar el cargo por ID
        db_trabajo = db.query(models.Trabajos).filter(models.Trabajos.trabajo_id == trabajo_id).first()
        # ❗ Si NO existe → error 404
        if not db_trabajo:
            raise HTTPException(status_code=404, detail="Cargo no encontrado")

        nombre_trabajo = db_trabajo.trabajo
        # Eliminar físicamente
        db.delete(db_trabajo)
        db.commit()

        return {
            "message": f"Trabajo '{nombre_trabajo}' eliminado correctamente",
        }

    except HTTPException:
        raise
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=f"Error en el servidor: {str(e)}")

@app.put("/api/deleteclientes/{cliente_id}", response_model=schemasclientes.DeleteClienteResponse)
async def delete_cliente(cliente_id: str, db: Session = Depends(get_db)):
    try:
        # Buscar el cliente por ID
        db_cliente = db.query(models.Clientes).filter(models.Clientes.cliente_id == cliente_id).first()
        # ❗ Si NO existe → error 404
        if not db_cliente:
            raise HTTPException(status_code=404, detail="Cargo no encontrado")

        nombre_cliente = db_cliente.clientes
        # Eliminar físicamente
        db.delete(db_cliente)
        db.commit()

        return {
            "message": f"Cliente '{nombre_cliente}' eliminado correctamente",
        }

    except HTTPException:
        raise
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=f"Error en el servidor: {str(e)}")

@app.put("/api/deletereportes/{serial_id}", response_model=schemasreportes.DeleteReportesResponse)
async def delete_reportes(serial_id: str, db: Session = Depends(get_db)):
    try:
        # Buscar el cliente por ID
        db_reporte = db.query(models.Reportes).filter(models.Reportes.serial_id == serial_id).first()
        # ❗ Si NO existe → error 404
        if not db_reporte:
            raise HTTPException(status_code=404, detail="Reporte no encontrado")
        nombre_empleado = db_reporte.clientes.clientes
        serial = db_reporte.seriales
        # Eliminar físicamente
        db.delete(db_reporte)
        db.commit()

        return {
            "message": f"Reporte {nombre_empleado} con serial {serial} ha sido eliminado correctamente",
        }

    except HTTPException:
        raise
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=f"Error en el servidor: {str(e)}")


@app.put("/api/deleteroles/{rol_id}", response_model=schemasroles.DeleteRolesResponse)
async def delete_roles(rol_id: str, db: Session = Depends(get_db)):
    try:
        # Buscar el rol por ID
        db_roles = db.query(models.Roles).filter(models.Roles.rol_id == rol_id).first()
        # ❗ Si NO existe → error 404
        if not db_roles:
            raise HTTPException(status_code=404, detail="Rol no encontrado")

        nombre_rol = db_roles.rol
        # Eliminar físicamente
        db.delete(db_roles)
        db.commit()

        return {
            "message": f"Rol '{nombre_rol}' eliminado correctamente",
        }

    except HTTPException:
        raise
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=f"Error en el servidor: {str(e)}")

@app.put("/api/deleteegresos/{egreso_id}", response_model=schemasegresos.DeleteEgresosResponse)
async def delete_egreso(egreso_id: str, db: Session = Depends(get_db)):
    try:
        # Buscar el rol por ID
        db_egreso = db.query(models.Egresos).filter(models.Egresos.egreso_id == egreso_id).first()
        # ❗ Si NO existe → error 404
        if not db_egreso:
            raise HTTPException(status_code=404, detail="Egreso no encontrado con el ID proporcionado")

        concepto = db_egreso.concepto
        # Eliminar físicamente
        db.delete(db_egreso)
        db.commit()

        db_saldos = db.query(models.Saldosiniciales).filter(models.Saldosiniciales.egreso_id == egreso_id).first()
         # ❗ Si NO existe → error 404
        if not db_saldos:
           raise HTTPException(status_code=404, detail="No se encontró saldosiniciales con el ID proporcionado")

        db.delete(db_saldos)
        db.commit()

        return {
            "message": f"Egreso '{concepto}' eliminado correctamente",
        }

    except HTTPException:
        raise
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=f"Error en el servidor: {str(e)}")

@app.put("/api/deleteingresos/{ingreso_id}", response_model=schemasingresos.DeleteIngresosResponse)
async def delete_egreso(ingreso_id: str, db: Session = Depends(get_db)):
    try:
        # Buscar el rol por ID
        db_ingreso = db.query(models.Ingresos).filter(models.Ingresos.ingreso_id == ingreso_id).first()
        # ❗ Si NO existe → error 404
        if not db_ingreso:
            raise HTTPException(status_code=404, detail="Ingreso no encontrado con el ID proporcionado")

        concepto = db_ingreso.concepto
        # Eliminar físicamente
        db.delete(db_ingreso)
        db.commit()

        db_saldos = db.query(models.Saldosiniciales).filter(models.Saldosiniciales.egreso_id == ingreso_id).first()
        # ❗ Si NO existe → error 404
        if not db_saldos:
           raise HTTPException(status_code=404, detail="No se encontró saldosiniciales con el ID proporcionado")

        db.delete(db_saldos)
        db.commit()
        return {
            "message": f"Ingreso {concepto} eliminado correctamente",
        }

    except HTTPException:
        raise
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=f"Error en el servidor: {str(e)}")


@app.put("/api/deleteempleados/{empleado_id}", response_model=schemasempleados.DeleteEmpleadosResponse)
async def delete_roles(empleado_id: str, db: Session = Depends(get_db)):
    try:
        # Buscar el rol por ID
        db_empleado = db.query(models.Empleados).filter(models.Empleados.empleado_id == empleado_id).first()
        # ❗ Si NO existe → error 404
        if not db_empleado:
            raise HTTPException(status_code=404, detail="Rol no encontrado")

        nombre_empleado = db_empleado.nombre
        # Eliminar físicamente
        db.delete(db_empleado)
        db.commit()

        return {
            "message": f"Empleado '{nombre_empleado}' eliminado correctamente",
        }

    except HTTPException:
        raise
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=f"Error en el servidor: {str(e)}")


@app.get("/")
async def root():
    return {"message": "Winter is coming."}


#------------------------ Poblar deopdown, Datatable ------------------------
@app.get("/api/cargarcargos", response_model=List[schemascargos.Cargoslist])
async def get_table_cargos(db: Session = Depends(get_db)):
           # Buscar tipo de trabajo que esté activo (flag = 1)
           cargos = db.query(models.Cargos).all()
           #cargos = db.query(models.Cargos).filter(models.Cargos.flag == 1).all()

           if not cargos:
                raise HTTPException(status_code=404, detail="Tipos de cargos no encontrados")
           return cargos

@app.get("/api/cargarmediopago", response_model=List[schemascarteraxcobrar.Mpagolist])
async def get_dropdownCuentabancaria(db: Session = Depends(get_db)):

           cuentabanacaria = db.query(models.Cuentabancaria).all()
           #cargos = db.query(models.Cargos).filter(models.Cargos.flag == 1).all()

           if not cuentabanacaria:
                raise HTTPException(status_code=404, detail="Tipos de cargos no encontrados")
           return cuentabanacaria

@app.get("/api/cargarcuentadestino", response_model=List[schemascuentadestino.Cdestinolist])
async def get_dropdownCuentadestino(db: Session = Depends(get_db)):

           cuentadestino = db.query(models.Cuentadestino).all()
           #cargos = db.query(models.Cargos).filter(models.Cargos.flag == 1).all()

           if not cuentadestino:
                raise HTTPException(status_code=404, detail="Tipos de cargos no encontrados")
           return cuentadestino

@app.get("/api/cargaroles", response_model=List[schemasroles.Roleslist])
async def get_paises(db: Session = Depends(get_db)):

           roles = db.query(models.Roles).all()
           if not roles:
                raise HTTPException(status_code=404, detail="Tipos de cargos no encontrados")
           return roles



@app.get("/api/cargartableroles", response_model=List[schemasroles.Roles])
async def get_table_roles(db: Session = Depends(get_db)):
           # Buscar tipo de trabajo que esté activo (flag = 1)
           roles = db.query(models.Roles).all()
           #cargos = db.query(models.Cargos).filter(models.Cargos.flag == 1).all()

           if not roles:
                raise HTTPException(status_code=404, detail="Tipos de roles no encontrados")
           return roles

@app.get("/api/cargartableperfil/{usuario_id}", response_model=List[schemas.Perfil])
async def get_table_perfiles(usuario_id: str,db: Session = Depends(get_db)):

           perfiles = db.query(models.User).filter(models.User.usuario_id == usuario_id).all()
           if not perfiles:
                raise HTTPException(status_code=404, detail="Tipos de perfiles no encontrados")
           return perfiles

@app.get("/api/cargartableegresos", response_model=List[schemasegresos.Egresos])
async def get_table_cargos(db: Session = Depends(get_db)):
           # Buscar tipo de trabajo que esté activo (flag = 1)
           egresos = db.query(models.Egresos).options(
                   joinedload(models.Egresos.usuario),
                   joinedload(models.Egresos.cuenta_destino)
           ).all()

           if not egresos:
                raise HTTPException(status_code=404, detail="Egresos no encontrados")
           return egresos

@app.get("/api/cargarestadisticaservicios")
async def get_table_estadistica(mes: str,db: Session = Depends(get_db)):
           # Buscar tipo de trabajo que esté activo (flag = 1)
           #mes ='10'
           print(f"❌ Error enviando correo a {mes}")

           servicios = db.query(models.Reportes).options(
                   joinedload(models.Reportes.usuario),
                   joinedload(models.Reportes.clientes),
                   joinedload(models.Reportes.trabajo)
           ).filter(models.Reportes.created_at.like(f"{mes}%")).all()

           if not servicios:
                raise HTTPException(status_code=404, detail="Estadisitica no encontrados")
           #return servicios

           resultado = {}
           for s in servicios:
               nombre = s.usuario.usuario_nombre if s.usuario else "Desconocido"
               if nombre not in resultado:
                   resultado[nombre] = []
               resultado[nombre].append({
                   "fecha": s.created_at.strftime("%Y-%m-%d"),
                   "servicio": s.trabajo.trabajo,
                   "cliente": s.clientes.clientes
               })

           # Convertimos a lista de objetos estructurados
           data_final = [
               {
                   "nombre": nombre,
                   "servicios": servicios
               }
               for nombre, servicios in resultado.items()
           ]

           # Ordenamos por cantidad de servicios (descendente)
           data_final.sort(key=lambda x: len(x["servicios"]), reverse=True)
           return data_final


@app.get("/api/cargarestadisticatrabajos")
async def get_table_estadistica(db: Session = Depends(get_db)):
           # Buscar tipo de trabajo que esté activo (flag = 1)
           mes ='2025-10'
           print(f"❌ Error enviando correo a {mes}")

           servicios = db.query(models.Reportes).options(
                   joinedload(models.Reportes.usuario),
                   joinedload(models.Reportes.clientes),
                   joinedload(models.Reportes.trabajo)
           ).filter(models.Reportes.created_at.like(f"{mes}%")).all()

           if not servicios:
                raise HTTPException(status_code=404, detail="Estadisitica no encontrados")
           #return servicios

           resultado = {}
           for s in servicios:
               #nombre = s.usuario.usuario_nombre if s.usuario else "Desconocido"
               trabajo = s.trabajo.trabajo if s.trabajo else "Desconocido"

               if trabajo not in resultado:
                   resultado[trabajo] = []
               resultado[trabajo].append({
                   "fecha": s.created_at.strftime("%Y-%m-%d"),
                   "usuario": s.usuario.usuario_nombre,
                   "cliente": s.clientes.clientes
               })

           # Convertimos a lista de objetos estructurados
           data_final = [
               {
                   "nombre": nombre,
                   "servicios": servicios
               }
               for nombre, servicios in resultado.items()
           ]

           # Ordenamos por cantidad de servicios (descendente)
           data_final.sort(key=lambda x: len(x["servicios"]), reverse=True)
           return data_final


@app.get("/api/cargartableingresos", response_model=List[schemasingresos.Ingresos])
async def get_table_ingresos(db: Session = Depends(get_db)):
           # Buscar tipo de trabajo que esté activo (flag = 1)
           ingresos = db.query(models.Ingresos).options(
                   joinedload(models.Ingresos.usuario),
                   joinedload(models.Ingresos.cuenta_destino)
           ).all()

           if not ingresos:
                raise HTTPException(status_code=404, detail="Ingresos no encontrados")
           return ingresos

@app.get("/api/cargartablecargos", response_model=List[schemascargos.Cargos])
async def get_table_cargos(db: Session = Depends(get_db)):
           # Buscar tipo de trabajo que esté activo (flag = 1)
           cargos = db.query(models.Cargos).all()
           #cargos = db.query(models.Cargos).filter(models.Cargos.flag == 1).all()

           if not cargos:
                raise HTTPException(status_code=404, detail="Tipos de cargos no encontrados")
           return cargos

@app.get("/api/cargartablepermisos")
async def get_table_permisos(db: Session = Depends(get_db)):
           # Buscar tipo de trabajo que esté activo (flag = 1)
           permisos = db.query(
               models.ControladoresPermisos.controladorpermiso_id,
               models.Roles.rol.label("rol"),
               models.Controladores.controlador.label("controlador"),
               models.ControladoresPermisos.ver,
               models.ControladoresPermisos.crear,
               models.ControladoresPermisos.editar,
               models.ControladoresPermisos.eliminar
           ).select_from(models.ControladoresPermisos)\
            .join(models.Controladores, models.ControladoresPermisos.controlador_id == models.Controladores.controlador_id)\
            .join(models.Roles, models.ControladoresPermisos.rol_id == models.Roles.rol_id)\
            .order_by(models.Roles.rol.asc())\
            .all()
           if not permisos:
                raise HTTPException(status_code=404, detail="Tipos de permisos no encontrados")
           return [
               {
                   "controladorID": p.controladorpermiso_id,
                   "rol": p.rol,
                   "controlador": p.controlador,
                   "ver": p.ver,
                   "crear": p.crear,
                   "editar": p.editar,
                   "eliminar": p.eliminar
               }
               for p in permisos
           ]


@app.get("/api/cargartabletrabajos", response_model=List[schemastrabajos.TrabajosA])
async def get_table_trabajo(db: Session = Depends(get_db)):

           trabajo = db.query(models.Trabajos).all()
           if not trabajo:
                raise HTTPException(status_code=404, detail="Tipos de cargos no encontrados")
           return trabajo


@app.get("/api/cargarpaises", response_model=List[schemasclientes.Paises])
async def get_paises(db: Session = Depends(get_db)):

           paises = db.query(models.Paises).all()
           if not paises:
                raise HTTPException(status_code=404, detail="Tipos de cargos no encontrados")
           return paises

@app.get("/api/cargarclientes", response_model=List[schemasclientes.ClientesWCD])
async def get_dropddownClientes(db: Session = Depends(get_db)):

           clientes = db.query(models.Clientes).all()
           if not clientes:
                raise HTTPException(status_code=404, detail="Clientes no encontrados")
           return clientes

@app.get("/api/cargartrabajos", response_model=List[schemasreportes.Trabajos])
async def get_dropdownTrabajos(db: Session = Depends(get_db)):

           trabajos = db.query(models.Trabajos).all()
           if not trabajos:
                raise HTTPException(status_code=404, detail="Clientes no encontrados")
           return trabajos

@app.get("/api/cargarestadocuenta", response_model=List[schemasestadocuenta.Estadocuentas])
async def get_dropdownEstadocuenta(db: Session = Depends(get_db)):

           estadocuenta = db.query(models.Estadocuentas).all()
           if not estadocuenta:
                raise HTTPException(status_code=404, detail="Estado de cuenta no encontrada")
           return estadocuenta

@app.get("/api/cargarempleados", response_model=List[schemasreportes.Empleados])
async def get_dropdownEmpleados(db: Session = Depends(get_db)):

           empleados = db.query(models.Empleados).all()
           if not empleados:
                raise HTTPException(status_code=404, detail="Clientes no encontrados")
           return empleados

@app.get("/api/cargartableclientes", response_model=List[schemasclientes.Clientes])
async def get_table_trabajo(db: Session = Depends(get_db)):

           trabajo = db.query(models.Clientes).all()
           if not trabajo:
                raise HTTPException(status_code=404, detail="Tipos de cargos no encontrados")
           return trabajo


@app.get("/api/estadisticas-generales")
def get_estadisticas(db: Session = Depends(get_db)):
    total_clientes = db.query(func.count(models.Clientes.cliente_id)).scalar() or 0
    total_usuarios = db.query(func.count(models.User.usuario_id)).scalar() or 0
    serviciosActivos = db.query(func.count(models.Reportes.serial_id))\
                    .filter(models.Reportes.flag == 1)\
                    .scalar()
    serviciosInactivos = db.query(func.count(models.Reportes.serial_id))\
                                        .filter(models.Reportes.flag == 0)\
                                        .scalar()
    return {
        "clientes": total_clientes,
        "serviciosInactivos": serviciosInactivos,
        "serviciosActivos": serviciosActivos,
        "usuarios": total_usuarios
    }

@app.get("/api/cargartablereportes/{usuario_id}", response_model=List[schemasreportes.Reportes])
async def get_table_reporte(usuario_id: str,db: Session = Depends(get_db)):

           reporte = db.query(models.Reportes).options(
                   joinedload(models.Reportes.usuario),
                   joinedload(models.Reportes.clientes),
                   joinedload(models.Reportes.trabajo),
                   joinedload(models.Reportes.estado)
           ).filter(models.Reportes.usuario_id == usuario_id).all()
           if not reporte:
                raise HTTPException(status_code=404, detail="Reportes no encontrados")
           return reporte

@app.get("/api/cargartablereportesfechas/{fechainicial}/{fechafinal}", response_model=List[schemasreportes.Reportes])
async def get_table_reporte(fechainicial: str,fechafinal: str,db: Session = Depends(get_db)):

           try:
                   # Convertir strings a objetos date
                   inicio = datetime.strptime(fechainicial, "%Y-%m-%d").date()
                   fin = datetime.strptime(fechafinal, "%Y-%m-%d").date()
           except ValueError:
                   raise HTTPException(status_code=400, detail="Formato de fecha inválido. Use YYYY-MM-DD")
           reporte = db.query(models.Reportes).options(
                   joinedload(models.Reportes.usuario),
                   joinedload(models.Reportes.clientes),
                   joinedload(models.Reportes.trabajo),
                   joinedload(models.Reportes.estado)
               ).filter(
                   and_(
                       func.date(models.Reportes.created_at) >= inicio,
                       func.date(models.Reportes.created_at) <= fin
                   )
               ).all()
           if not reporte:
                raise HTTPException(status_code=404, detail="Reportes no encontrados")
           return reporte

@app.get("/api/cargartablecarteraxcobrar", response_model=List[schemascarteraxcobrar.Carteraxcobrar])
async def get_table_carteraxcobrar(db: Session = Depends(get_db)):

           reporte = (
               db.query(
                   models.Clientes.cliente_id.label("cliente_id"),
                   models.Clientes.clientes.label("clientes"),
                   func.sum(models.Carteraxcobrar.debe).label("debe"),
                   func.sum(models.Carteraxcobrar.haber).label("haber"),
                   (func.sum(models.Carteraxcobrar.debe) - func.sum(models.Carteraxcobrar.haber)).label("saldo"),
               )
               .join(models.Clientes, models.Carteraxcobrar.cliente_id == models.Clientes.cliente_id)
               .group_by(models.Clientes.clientes)
               .all()
           )

           if not reporte:
                raise HTTPException(status_code=404, detail="Reportes no encontrados")
           return reporte

@app.get("/api/cargartableservicioxcobrar/{cliente_id}", response_model=List[schemasreportes.Reportes])
async def get_table_servicioxcobrar(cliente_id: str,db: Session = Depends(get_db)):

           reporte = db.query(models.Reportes).options(
               joinedload(models.Reportes.usuario),
               joinedload(models.Reportes.clientes),
               joinedload(models.Reportes.trabajo),
               joinedload(models.Reportes.estado),
           ).filter(models.Reportes.cliente_id == cliente_id).all()

           if not reporte:
                raise HTTPException(status_code=404, detail="Reportes no encontrados")
           return reporte

@app.get("/api/cargartablesaldos", response_model=List[schemassaldos.Saldos])
async def get_table_Saldos(db: Session = Depends(get_db)):

          reporte = db.query(models.Saldosiniciales).options(
                    joinedload(models.Saldosiniciales.usuario),
                    joinedload(models.Saldosiniciales.cuenta_destino)
          ).all()
          if not reporte:
               raise HTTPException(status_code=404, detail="Reportes no encontrados")
          return reporte

@app.get("/api/cargartableempleados", response_model=List[schemasempleados.Empleados])
async def get_table_empleados(db: Session = Depends(get_db)):

           #empleado = db.query(models.Empleados).all()
           empleados = db.query(models.Empleados).options(
                   joinedload(models.Empleados.cargo),
                   joinedload(models.Empleados.rol)
               ).all()

           if not empleados:
                raise HTTPException(status_code=404, detail="Empleados no encontrados")
           return empleados



@app.get("/api/cargarserialcliente/{cliente_id}", response_model=List[schemasreportes.SerialesReportesResponse])
async def get_seriales(cliente_id: str, db: Session = Depends(get_db)):
    try:
        # Buscar el rol por ID
        db_seriales = (db.query(
        models.Reportes.serial_id,
        models.Reportes.seriales).filter(models.Reportes.cliente_id == cliente_id)
        .distinct(models.Reportes.seriales)  # ← Elimina duplicados
        .all()
        )
        # ❗ Si NO existe → error 404
        if not db_seriales:
            raise HTTPException(status_code=404, detail="Seriales no encontrado")

        return db_seriales

    except HTTPException:
        raise
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=f"Error en el servidor: {str(e)}")



#-------------------------- Validar email de registros---------------------------------------------
@app.get("/api/verify-email")
async def verify_email(token: str, db: Session = Depends(get_db)):
    user = db.query(models.User).filter(models.User.usuario_unico == token).first()
    if not user:
        raise HTTPException(status_code=404, detail="Token inválido")

    user.email_verified = 1
    user.usuario_estado = 1
    db.commit()

    #return {"message": "✅ ¡Correo verificado con éxito! Ya puedes iniciar sesión."}
    # ✅ Redirigir al login en el frontend
    frontend_url = os.getenv("CORS_ORIGINS", "http://localhost:5173")
    return RedirectResponse(url=f"{frontend_url}/api/auth/login")

def send_verification_email(to_email: str, verification_link: str,usuario_nombre: str) -> bool:
    """
    Envía un correo de verificación al usuario.
    Retorna True si se envió correctamente, False si falló.
    """
    try:
        # Configuración SMTP
        smtp_server = os.getenv("SMTP_SERVER")
        smtp_port = int(os.getenv("SMTP_PORT", 587))
        smtp_username = os.getenv("SMTP_USERNAME")
        smtp_password = os.getenv("SMTP_PASSWORD")
        frontend_url = os.getenv("FRONTEND_URL", "http://localhost:5173")

        # Crear mensaje
        message = MIMEMultipart("alternative")
        message["Subject"] = "Verifica tu correo - Makinelab"
        message["From"] = smtp_username
        message["To"] = to_email

        # Contenido HTML
        html = f"""
        <html>
          <body style="margin:0; padding:0; background-color:#f4f6f8; font-family:Arial, sans-serif;">
            <table width="100%" border="0" cellspacing="0" cellpadding="0" style="background-color:#f4f6f8; padding:20px 0;">
              <tr>
                <td align="center">
                  <table width="600" border="0" cellspacing="0" cellpadding="0" style="background-color:#ffffff; border-radius:8px; padding:40px; text-align:center; box-shadow:0 4px 12px rgba(0,0,0,0.08);">
                    <tr>
                      <td style="font-size:24px; font-weight:bold; color:#0b2b4a; padding-bottom:12px;">
                        ¡Bienvenido: {usuario_nombre}!
                      </td>
                    </tr>

                    <tr>
                      <td style="font-size:16px; color:#4a5568; padding-bottom:20px;">
                        Gracias por registrarte en nuestra aplicación.
                      </td>
                    </tr>
                    <tr>
                      <td style="font-size:15px; color:#4a5568; padding-bottom:20px;">
                        Por favor, haz clic en el botón para verificar tu correo:
                      </td>
                    </tr>
                    <tr>
                      <td>
                        <a href="{verification_link}" style="
                            display:inline-block;
                            background-color:#3b82f6;
                            color:#ffffff;
                            text-decoration:none;
                            padding:12px 28px;
                            border-radius:30px;
                            font-weight:bold;
                            font-size:16px;
                            box-shadow:0 4px 10px rgba(59,130,246,0.3);
                        ">Verificar correo</a>
                      </td>
                    </tr>
                    <tr>
                      <td style="font-size:14px; color:#718096; padding-top:30px;">
                        Si no solicitaste este registro, ignora este mensaje.
                      </td>
                    </tr>
                    <tr>
                      <td style="font-size:14px; color:#4a5568; padding-top:12px;">
                        Saludos,<br><strong>EQUIPO DE MAKINELAB</strong>
                      </td>
                    </tr>
                  </table>
                </td>
              </tr>
            </table>
          </body>
        </html>
        """


        # Adjuntar HTML
        message.attach(MIMEText(html, "html"))

        # Enviar
        context = ssl.create_default_context()
        with smtplib.SMTP(smtp_server, smtp_port) as server:
            server.starttls(context=context)
            server.login(smtp_username, smtp_password)
            server.sendmail(smtp_username, to_email, message.as_string())

        return True

    except Exception as e:
        print(f"❌ Error enviando correo a {to_email}: {str(e)}")
        return False