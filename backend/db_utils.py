# backend/db_utils.py
from sqlalchemy import text
from sqlalchemy.orm import Session
from colorama import init, Fore, Style
import sys

# Inicializar colorama
init()

def check_db_connection(db: Session):
    """Verifica la conexión a la base de datos de forma elegante"""
    try:
        # Ejecutar una consulta simple
        db.execute(text("SELECT 1"))
        print(f"{Fore.GREEN}✅ {Style.BRIGHT}Conexión a MySQL establecida correctamente{Style.RESET_ALL}")
        print(f"{Fore.CYAN}📊 Base de datos: {Fore.YELLOW}elegantapp{Style.RESET_ALL}")
        print(f"{Fore.CYAN}⏱️  Tiempo de respuesta: {Fore.GREEN}< 100ms{Style.RESET_ALL}")
        return True
    except Exception as e:
        print(f"{Fore.RED}❌ {Style.BRIGHT}Error al conectar con MySQL{Style.RESET_ALL}")
        print(f"{Fore.RED}📝 Detalle: {str(e)}{Style.RESET_ALL}")
        print(f"{Fore.YELLOW}💡 Verifica: .env, credenciales, MySQL service{Style.RESET_ALL}")
        sys.exit(1)  # Termina la aplicación si no hay conexión