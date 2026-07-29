import os
from dotenv import load_dotenv

load_dotenv()   # Cargamos variables de entorno desde .env
DB_URI = os.getenv("DB_URI")   # Obtenemos la URI de la base de datos de nuestro .env

# Definimos la clase base de configuración
class Config:
    SQLALCHEMY_DATABASE_URI = DB_URI
    SQLALCHEMY_TRACK_MODIFICATIONS = False

# Creamos clases para cada entorno que se utilice.
class DevelopConfig(Config):
    DEBUG = True