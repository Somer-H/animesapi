import pymysql
import os
import re
from dotenv import load_dotenv

load_dotenv()
DATABASE_URL = os.getenv("DATABASE_URL")

# Extraer credenciales de la URL de DATABASE_URL
pattern = r"mysql\+pymysql://(.*):(.*)@(.*):(\d+)/(.*)"
match = re.match(pattern, DATABASE_URL)

if not match:
    print("Error: No se pudo parsear DATABASE_URL")
    exit()

user, password, host, port, db_name = match.groups()

print(f"Conectando a {host} para añadir columna 'image_url'...")

try:
    connection = pymysql.connect(
        host=host,
        user=user,
        password=password,
        db=db_name,
        port=int(port),
        connect_timeout=10,
        autocommit=True
    )
    
    with connection.cursor() as cursor:
        # Verificar si la columna ya existe para evitar errores
        cursor.execute("SHOW COLUMNS FROM animes LIKE 'image_url'")
        result = cursor.fetchone()
        
        if not result:
            cursor.execute("ALTER TABLE animes ADD COLUMN image_url VARCHAR(500) AFTER descripcion")
            print("¡ÉXITO! Columna 'image_url' añadida a la tabla 'animes'.")
        else:
            print("La columna 'image_url' ya existe.")

    connection.close()
except Exception as e:
    print(f"Error al modificar la tabla: {e}")
