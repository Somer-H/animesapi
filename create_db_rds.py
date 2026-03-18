import pymysql
import os
import re
from dotenv import load_dotenv

load_dotenv()
DATABASE_URL = os.getenv("DATABASE_URL")

pattern = r"mysql\+pymysql://(.*):(.*)@(.*):(\d+)/(.*)"
match = re.match(pattern, DATABASE_URL)
user, password, host, port, db_name = match.groups()

print(f"Intentando conectar a {host} SIN SSL...")

try:
    connection = pymysql.connect(
        host=host,
        user=user,
        password=password,
        port=int(port),
        connect_timeout=10,
        autocommit=True
    )
    
    with connection.cursor() as cursor:
        cursor.execute(f"CREATE DATABASE IF NOT EXISTS {db_name}")
        print(f"¡ÉXITO! Base de datos '{db_name}' lista.")
    connection.close()
except Exception as e:
    print(f"Error sin SSL: {e}")
