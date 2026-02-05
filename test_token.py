from datetime import datetime, timedelta, timezone
from jose import JWTError, jwt
from config.settings import SECRET_KEY, ALGORITHM, ACCESS_TOKEN_EXPIRE_MINUTES

print("=" * 50)
print("DEBUGUANDO TOKENS JWT")
print("=" * 50)

# 1. Verificar configuración
print(f"\n1. CONFIGURACIÓN:")
print(f"   SECRET_KEY: {SECRET_KEY[:30]}...")
print(f"   ALGORITHM: {ALGORITHM}")
print(f"   TOKEN EXPIRA EN: {ACCESS_TOKEN_EXPIRE_MINUTES} minutos")

# 2. Crear un token de prueba
print(f"\n2. CREANDO TOKEN DE PRUEBA...")
data = {"sub": "1"}  # ← CAMBIO: Convertir a STRING
expire = datetime.now(timezone.utc) + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
to_encode = data.copy()
to_encode.update({"exp": expire.timestamp()})

print(f"   Data a codificar: {to_encode}")
print(f"   Expiración (timestamp): {expire.timestamp()}")
print(f"   Expiración (datetime): {expire}")

token = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
print(f"\n   TOKEN GENERADO:")
print(f"   {token}")

# 3. Intentar decodificar el token
print(f"\n3. DECODIFICANDO TOKEN...")
try:
    payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
    print(f"   ✅ TOKEN VÁLIDO")
    print(f"   Payload: {payload}")
    print(f"   Usuario ID (sub): {payload.get('sub')}")
except JWTError as e:
    print(f"   ❌ ERROR AL DECODIFICAR:")
    print(f"   {type(e).__name__}: {str(e)}")

print("\n" + "=" * 50)
