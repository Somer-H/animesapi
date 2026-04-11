import mysql.connector
import os
from dotenv import load_dotenv

# Cargar variables de entorno
load_dotenv()

# Configuración de la base de datos desde URL (mysql+pymysql://user:pass@host:port/db)
db_url = os.getenv("DATABASE_URL")
# Parsear la URL (muy básico)
# mysql+pymysql://somer:140823schmesom1917@anime.crq4swmsoc3a.us-east-1.rds.amazonaws.com:3306/animes
parts = db_url.replace("mysql+pymysql://", "").replace("@", ":").replace("/", ":").split(":")
user = parts[0]
password = parts[1]
host = parts[2]
port = parts[3]
database = parts[4]

try:
    conn = mysql.connector.connect(
        host=host,
        user=user,
        password=password,
        port=port,
        database=database
    )
    cursor = conn.cursor()

    # 1. Obtener el ID del primer usuario
    cursor.execute("SELECT id FROM users LIMIT 1")
    first_user = cursor.fetchone()
    if not first_user:
        print("Error: No hay usuarios en la base de datos para asignar los animes.")
        exit(1)
    
    user_id = first_user[0]
    print(f"Usando User ID {user_id} para animes existentes.")

    # 2. Añadir la columna user_id
    # Intentamos añadirla, si ya existe el error será capturado
    try:
        cursor.execute(f"ALTER TABLE animes ADD COLUMN user_id INT NULL")
        print("Columna 'user_id' añadida.")
    except Exception as e:
        if "Duplicate column name" in str(e):
            print("La columna 'user_id' ya existe.")
        else:
            raise e

    # 3. Asignar el user_id a los registros que lo tengan null
    cursor.execute(f"UPDATE animes SET user_id = {user_id} WHERE user_id IS NULL")
    print(f"Registros actualizados con user_id = {user_id}.")

    # 4. Hacer la columna NOT NULL
    cursor.execute("ALTER TABLE animes MODIFY COLUMN user_id INT NOT NULL")
    print("Columna 'user_id' establecida como NOT NULL.")

    # 5. Añadir la FK
    try:
        cursor.execute("ALTER TABLE animes ADD CONSTRAINT fk_anime_user FOREIGN KEY (user_id) REFERENCES users(id)")
        print("Relación Foreing Key añadida.")
    except Exception as e:
        if "Duplicate key name" in str(e) or "Multiple foreign key constraints" in str(e):
            print("La relación FK ya existe.")
        else:
            print(f"Nota: No se pudo añadir la FK (posiblemente ya existe): {e}")

    conn.commit()
    print("Migración completada exitosamente.")

except Exception as e:
    print(f"Error durante la migración: {e}")
finally:
    if 'conn' in locals() and conn.is_connected():
        cursor.close()
        conn.close()
