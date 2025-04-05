import hashlib
import os
import json

def generar_sal():
    return os.urandom(16).hex()

def hashear_password(password, sal_hex):
    sal = bytes.fromhex(sal_hex)
    password_hasheado = hashlib.pbkdf2_hmac('sha256', password.encode('utf-8'), sal, 100000)
    return password_hasheado.hex()

# Ejemplo para crear un usuario:
nombre_usuario = "LETI"
password = "123"
sal_generada = generar_sal()
hash_generado = hashear_password(password, sal_generada)

print(f"Nombre de usuario: {nombre_usuario}")
print(f"Sal (hex): {sal_generada}")
print(f"Hash: {hash_generado}")

# Repite esto para cada usuario que quieras añadir.
# Luego, crea el archivo usuarios_seguros.json con la estructura mostrada anteriormente,
# usando la sal y el hash generados para cada usuario.