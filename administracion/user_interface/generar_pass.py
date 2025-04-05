import os
import hashlib

def generar_sal():
    return os.urandom(16)

def hashear_contrasena_con_sal(contrasena, sal):
    contrasena_bytes = contrasena.encode('utf-8')
    sal_bytes = sal
    objeto_hash = hashlib.sha256(sal_bytes + contrasena_bytes)
    contrasena_hasheada = objeto_hash.hexdigest()
    return contrasena_hasheada, sal

# Especifica el nombre de usuario para el que quieres crear la contraseña
nombre_usuario = "LETI"  # Reemplaza "test" con el usuario que quieras

# Especifica la contraseña que quieres usar
contrasena_deseada = "123"  # Reemplaza con la contraseña que quieras

# Genera una nueva sal
sal_generada = generar_sal()

# Hashea la contraseña con la sal generada
contrasena_hasheada, _ = hashear_contrasena_con_sal(contrasena_deseada, sal_generada)

# Imprime la sal y el hash para que puedas copiarlos
print(f"Sal para el usuario '{nombre_usuario}' (en hexadecimal): {sal_generada.hex()}")
print(f"Hash para el usuario '{nombre_usuario}': {contrasena_hasheada}")