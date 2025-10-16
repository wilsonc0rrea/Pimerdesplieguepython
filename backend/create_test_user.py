# backend/create_test_user.py
from sqlalchemy.orm import Session
from database import SessionLocal
import models
import security

def create_test_user():
    db = SessionLocal()
    try:
        # Verificar si ya existe
        existing_user = db.query(models.User).filter(models.User.email == "admin@example.com").first()
        if not existing_user:
            hashed_password = security.get_password_hash("admin123")
            user = models.User(
                email="admin@example.com",
                hashed_password=hashed_password,
                full_name="Administrador",
                is_active=True
            )
            db.add(user)
            db.commit()
            print("✅ Usuario de prueba creado: admin@example.com / admin123")
        else:
            print("ℹ️  Usuario de prueba ya existe")
    finally:
        db.close()

if __name__ == "__main__":
    create_test_user()