import os
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from dotenv import load_dotenv

# Esto solo cargará el .env si el archivo existe (local)
# Si no existe (Railway), simplemente no hará nada y pasará a buscar en el sistema
load_dotenv() 

# Buscamos la variable en el entorno del sistema
SQLALCHEMY_DATABASE_URL = os.getenv("DATABASE_URL")

# --- SOLUCIÓN AL ERROR ---
# Añadimos una verificación de seguridad
if SQLALCHEMY_DATABASE_URL is None:
    raise ValueError("Error: La variable DATABASE_URL no está configurada en Railway o en el .env")

engine = create_engine(SQLALCHEMY_DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()
