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
from fastapi import FastAPI, Depends, HTTPException, status, Response
from fastapi.responses import JSONResponse
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
from sqlalchemy.orm import Session
# -------------------------------------------------------------------
# 🛠️ Importamos 'text' de SQLAlchemy para ejecutar SQL crudo de forma segura.
# Útil cuando necesitas consultas complejas que el ORM no cubre bien.
# ¡NUNCA concatenes strings SQL! Usa 'text()' con parámetros para evitar inyecciones.
# Ejemplo: db.execute(text("SELECT * FROM users WHERE age > :age"), {"age": 18})
# -------------------------------------------------------------------
from sqlalchemy import text
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
CORS_ORIGINS = os.getenv("CORS_ORIGINS", "http://localhost:5173").split(",")
# -------------------------------------------------------------------
# 🔑 SECRET_KEY: Clave secreta usada para firmar tokens (JWT), sesiones, cookies, etc.
# - DEBE ser única, larga y aleatoria (ej: generada con `openssl rand -hex 32`).
# - NO debe estar en código fuente ni en repositorios públicos.
# - Si no se define en .env, la aplicación debería fallar (no hay valor por defecto).
# - Ejemplo de uso: firmar tokens JWT con `python-jose` o `passlib`.
# -------------------------------------------------------------------
SECRET_KEY = os.getenv("SECRET_KEY")
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
import schemas,schemasreportes,schemascargos,schemastrabajos
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
    allow_origins=CORS_ORIGINS,
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
       "command": "logout"
    },
    {
        "label": "Inicio",
        "icon": "pi pi-home",
        "to": "/"
    },
    {
        "label": "Usuarios",
        "icon": "pi pi-users",
        "items": [
            {
                "label": "Lista",
                "icon": "pi pi-list",
                "to": "/usuarios/lista"
            },
            {
                "label": "Crear",
                "icon": "pi pi-plus",
                "to": "/usuarios/crear"
            },
            {
                "label": "Reportes",
                "icon": "pi pi-chart-bar",
                "items": [
                    {"label": "Diarios", "icon": "pi pi-calendar", "to": "/usuarios/reportes/diarios"},
                    {"label": "Mensuales", "icon": "pi pi-calendar-plus", "to": "/usuarios/reportes/mensuales"}
                ]
            }
        ]
    },
    {
        "label": "Configuración",
        "icon": "pi pi-cog",
        "items": [
            {
               "label": "Maestros",
               "icon": "pi pi-plus",
               "items": [
                   {"label": "Reportes", "icon": "pi pi-check-circle", "to": "/config/reportes"},
                   {"label": "Cargos", "icon": "pi pi-check-circle", "to": "/config/cargos"},
                   {"label": "Tipos", "icon": "pi pi-check-circle", "to": "/config/ttrabajos"},
                   {"label": "Clientes", "icon": "pi pi-check-circle", "to": "/config/clientes"},
               ]
            },

            {"label": "Roles", "icon": "pi pi-plus", "to": "/config/roles"},
            {"label": "Permisos", "icon": "pi pi-plus", "to": "/config/permisos"},
            {"label": "Motores", "icon": "pi pi-plus", "to": "/config/motores"},
            {"label": "Precios", "icon": "pi pi-plus", "to": "/config/precios"},
            {"label": "Perfil", "icon": "pi pi-plus", "to": "/config/perfil"},
            {"label": "Sistema", "icon": "pi pi-server", "to": "/config/sistema"},

        ]
    }
]

# --- Rutas ---
@app.get("/api/menu")
async def get_menu():
    return MENU_DATA

@app.post("/api/login", response_model=schemas.Token)
async def login(user: schemas.LoginIn, db: Session = Depends(get_db)):

        # 1. Buscar usuario por email
        db_user = db.query(models.User).filter(models.User.usuario_email == user.usuario_email).first()
        if not db_user:
            raise HTTPException(status_code=404, detail="Usuario no encontrado")

        # 2. Verificar contraseña
        if not security.verify_password(user.usuario_password, db_user.usuario_password):
            raise HTTPException(status_code=401, detail="Contraseña inconrrecta")
        print("el usuario entró", user)
        # 3. Crear tokens
        access_token = security.create_access_token(data={"sub": user.usuario_email})
        print("el token", access_token)
        # 4. Respuesta con cookie y datos de usuario
        response = JSONResponse(
            content={
                "usuario_id": db_user.usuario_id,
                "usuario_nombre": db_user.usuario_nombre,
                "usuario_email": db_user.usuario_email,
                "usuario_estado": db_user.usuario_estado,
                "token": {"access_token": access_token,"token_type": "bearer"}
            }
        )
        #set_refresh_cookie(response, refresh_token, expires_days=7)
        return response

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
            usuario_estado=1,
            created_at=datetime.now(colombia_tz)  # ¡Corregido! Era solo "datetime"
        )

        db.add(new_user)
        db.commit()
        db.refresh(new_user)
        print(f"✅ ¡Usuario {new_user.usuario_email} creado exitosamente!")
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
        print(f"✅ ¡Usuario {new_user.usuario_email} creado exitosamente!")
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

#-------------------------- Seccion de eliminar ---------------------------------
@app.put("/api/deletecargos/{cargo_id}", response_model=schemascargos.DeleteCargoResponse)
async def delete_cargo(cargo_id: str, db: Session = Depends(get_db)):
    try:
        # Buscar el cargo por ID
        db_cargo = db.query(models.Cargos).filter(models.Cargos.cargo_id == cargo_id).first()
        # ❗ Si NO existe → error 404
        if not db_cargo:
            raise HTTPException(status_code=404, detail="Cargo no encontrado")

        # Eliminar físicamente
        db.delete(db_cargo)
        db.commit()

        return {
            "message": f"Cargo '{db_cargo.cargo}' eliminado correctamente",
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

        # Eliminar físicamente
        db.delete(db_trabajo)
        db.commit()

        return {
            "message": f"Cargo '{db_trabajo.trabajo}' eliminado correctamente",
        }

    except HTTPException:
        raise
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=f"Error en el servidor: {str(e)}")


@app.get("/api/health")
async def health(db: Session = Depends(get_db)):
    try:
        db.execute(text("SELECT 1"))
        return {
            "status": "ok",
            "database": "connected",
            "message": "✅ Todo funciona correctamente"
        }
    except Exception as e:
        return {
            "status": "error",
            "database": "disconnected",
            "message": "❌ Error en la conexión a la base de datos",
            "error": str(e)
        }


@app.get("/")
async def root():
    return {"message": "Winter is coming."}



#------------------------ Poblar deopdown, Datatable ------------------------
@app.get("/api/cargartablecargos", response_model=List[schemascargos.Cargos])
async def get_table_cargos(db: Session = Depends(get_db)):
           # Buscar tipo de trabajo que esté activo (flag = 1)
           cargos = db.query(models.Cargos).all()
           #cargos = db.query(models.Cargos).filter(models.Cargos.flag == 1).all()

           if not cargos:
                raise HTTPException(status_code=404, detail="Tipos de cargos no encontrados")
           return cargos

@app.get("/api/cargartabletrabajos", response_model=List[schemastrabajos.TrabajosA])
async def get_table_trabajo(db: Session = Depends(get_db)):

           print("✅ Cargando tabla trabajos...")
           trabajo = db.query(models.Trabajos).all()
           print(f"✅ ¡Usuario {trabajo} creado exitosamente!")
           if not trabajo:
                raise HTTPException(status_code=404, detail="Tipos de cargos no encontrados")
           return trabajo