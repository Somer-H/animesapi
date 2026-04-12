"""
Script de migración para el sistema de Tags.

Cambios que aplica:
1. Añade columna 'tags' (VARCHAR 500, nullable) a la tabla 'animes'
2. Crea la tabla 'user_tag_subscriptions'

Ejecutar: python migrate_tags.py
"""
import mysql.connector
import os
from dotenv import load_dotenv

load_dotenv()

db_url = os.getenv("DATABASE_URL")
parts = db_url.replace("mysql+pymysql://", "").replace("@", ":").replace("/", ":").split(":")
db_user = parts[0]
password = parts[1]
host = parts[2]
port = parts[3]
database = parts[4]

try:
    conn = mysql.connector.connect(
        host=host,
        user=db_user,
        password=password,
        port=port,
        database=database
    )
    cursor = conn.cursor()

    # ─── 1. Columna 'tags' en animes ────────────────────────────────────────
    try:
        cursor.execute("ALTER TABLE animes ADD COLUMN tags VARCHAR(500) NULL DEFAULT ''")
        print("✅ Columna 'tags' añadida a la tabla 'animes'.")
    except Exception as e:
        if "Duplicate column name" in str(e):
            print("ℹ️  Columna 'tags' ya existe en 'animes'.")
        else:
            raise e

    # ─── 2. Tabla user_tag_subscriptions ────────────────────────────────────
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS user_tag_subscriptions (
            id INT AUTO_INCREMENT PRIMARY KEY,
            user_id INT NOT NULL,
            tag VARCHAR(100) NOT NULL,
            fcm_token VARCHAR(300) NULL,
            created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
            UNIQUE KEY uq_user_tag (user_id, tag),
            CONSTRAINT fk_tag_sub_user FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE
        )
    """)
    print("✅ Tabla 'user_tag_subscriptions' creada (o ya existía).")

    conn.commit()
    print("\n🎉 Migración de tags completada exitosamente.")

except Exception as e:
    print(f"❌ Error durante la migración: {e}")
finally:
    if 'conn' in locals() and conn.is_connected():
        cursor.close()
        conn.close()
