# backend/security.py
from passlib.context import CryptContext
import os
import jwt
from jwt.exceptions import InvalidTokenError as JWTError
from datetime import datetime, timedelta
from fastapi import Request, Depends

#pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
pwd_context = CryptContext(schemes=["argon2"], deprecated="auto")

def get_password_hash(password):
    return pwd_context.hash(password)

def verify_password(password: str, hashed_password: str) -> bool:
    return pwd_context.verify(password, hashed_password)


# ✅ Ya están disponibles porque load_dotenv() se llamó en main.py
SECRET_KEY = os.getenv("SECRET_KEY")
ALGORITHM = os.getenv("ALGORITHM")
ACCESS_TOKEN_EXPIRE_MINUTES = 60

def create_access_token(data: dict):
    to_encode = data.copy()
    expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({
    "exp": expire,
    "iat": datetime.utcnow(),    # (issued at)
    "nbf": datetime.utcnow(),    # (not before)
    })

    #asegurarnos que existe un "sub"
    if "sub" not in to_encode:
        raise ValueError("El token debe incluir el campo 'sub' con el ID o email del usuario")

    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt
    #return {"access_token": encoded_jwt,"token_type": "bearer"}

def generate_refresh_token():
    # token value returned to client (random)
    token = os.urandom(32).hex()
    # store hashed version in DB
    token_hash = hashlib.sha256(token.encode()).hexdigest()
    return token, token_hash

def get_current_user_from_cookie(request: Request):
    token = request.cookies.get("access_token")
    if not token:
        raise HTTPException(status_code=401, detail="No autenticado")
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        return payload.get("sub")
    except PyJWTError:
        raise HTTPException(status_code=401, detail="Token inválido o expirado")