import os
from contextlib import contextmanager
import mysql.connector
from dotenv import load_dotenv

load_dotenv()

@contextmanager
def conexion():
    cn = None
    try:
        cn = mysql.connector.connect(
            host= os.getenv("DB_HOST", "localhost"),
            port= int(os.getenv("DB_PORT", "3306")),
            user= os.getenv("DB_USER"),
            password= os.getenv("DB_PASSWORD"), 
            database= os.getenv("DB_NAME"),
        )
        yield cn
    finally:
        if cn and cn.is_connected():
            cn.close()