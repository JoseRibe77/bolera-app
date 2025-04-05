import sqlite3
import datetime
import hashlib
import time

def inicializar_base_de_datos():
    conn = sqlite3.connect('bolera.db')
    cursor = conn.cursor()

    # Crear la tabla de roles si no existe
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS roles (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT UNIQUE NOT NULL
        )
    ''')

    # Crear la tabla de pistas si no existe
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS pistas (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            numero_pista INTEGER UNIQUE,
            estado TEXT
        )
    ''')

    # Crear la tabla de juegos si no existe
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS juegos (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            lane_number INTEGER,
            start_time TEXT,
            end_time TEXT,
            game_type TEXT
        )
    ''')

    # Crear la tabla de jugadores por juego si no existe
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS jugadores_por_juego (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            game_id INTEGER,
            player_name TEXT,
            score INTEGER,
            photo_path TEXT,
            FOREIGN KEY (game_id) REFERENCES juegos(id)
        )
    ''')

    # Crear la tabla de registro de administradores si no existe
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS administradores_log (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            timestamp TEXT,
            admin_name TEXT,
            action TEXT
        )
    ''')

    # Crear la tabla de usuarios si no existe
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS usuarios (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT UNIQUE NOT NULL,
            password TEXT NOT NULL,
            role_id INTEGER NOT NULL,
            last_login TEXT,
            FOREIGN KEY (role_id) REFERENCES roles(id)
        )
    ''')

    conn.commit()
    conn.close()
    print("inicializar_base_de_datos() completado.")

def conectar_base_de_datos():
    return sqlite3.connect('bolera.db')

def crear_usuario(username, password, role_id):
    conn = sqlite3.connect('bolera.db')
    cursor = conn.cursor()

    hashed_password = hashlib.sha256(password.encode('utf-8')).hexdigest()

    try:
        cursor.execute('''
            INSERT INTO usuarios (username, password, role_id)
            VALUES (?, ?, ?)
        ''', (username, hashed_password, role_id))
        conn.commit()
        conn.close()
        print("crear_usuario('{}', ..., {}) completado. Hash: {}".format(username, role_id, hashed_password))
        return True
    except sqlite3.IntegrityError:
        print("El usuario '{}' ya existe.".format(username))
        conn.close()
        return False

def verificar_password(plain_password, hashed_password):
    hashed_input = hashlib.sha256(plain_password.encode('utf-8')).hexdigest()
    return hashed_input == hashed_password

def insertar_roles_iniciales():
    conn = sqlite3.connect('bolera.db')
    cursor = conn.cursor()
    roles_iniciales = ['administrador', 'encargado', 'superusuario', 'usuario']
    print("insertar_roles_iniciales() comenzando...")
    for role in roles_iniciales:
        try:
            cursor.execute("INSERT INTO roles (name) VALUES (?)", (role,))
            print("Rol '{}' insertado.".format(role))
        except sqlite3.IntegrityError:
            print("El rol '{}' ya existe.".format(role))
    conn.commit()
    conn.close()
    print("insertar_roles_iniciales() completado.")

def obtener_rol_id_por_nombre(role_name):
    conn = sqlite3.connect('bolera.db')
    cursor = conn.cursor()
    print("obtener_rol_id_por_nombre('{}') comenzando...".format(role_name))
    cursor.execute("SELECT id FROM roles WHERE name = ?", (role_name,))
    result = cursor.fetchone()
    conn.close()
    if result:
        print("obtener_rol_id_por_nombre('{}') devolvió ID: {}".format(role_name, result[0]))
        return result[0]
    else:
        print("obtener_rol_id_por_nombre('{}') no encontró el rol.".format(role_name))
        return None

def crear_nuevo_juego(lane_number, start_time, game_type):
    conn = sqlite3.connect('bolera.db')
    cursor = conn.cursor()

    cursor.execute('''
        INSERT INTO juegos (lane_number, start_time, game_type)
        VALUES (?, ?, ?)
    ''', (lane_number, start_time, game_type))

    conn.commit()
    conn.close()
    return cursor.lastrowid

def registrar_accion_administrador(admin_name, action):
    conn = sqlite3.connect('bolera.db')
    cursor = conn.cursor()

    timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    cursor.execute('''
        INSERT INTO administradores_log (timestamp, admin_name, action)
        VALUES (?, ?, ?)
    ''', (timestamp, admin_name, action))

    conn.commit()
    conn.close()

def agregar_jugador_a_juego(game_id, player_name, score=0):
    conn = sqlite3.connect('bolera.db')
    cursor = conn.cursor()

    cursor.execute('''
        INSERT INTO jugadores_por_juego (game_id, player_name, score)
        VALUES (?, ?, ?)
    ''', (game_id, player_name, score))

    conn.commit()
    conn.close()

def obtener_jugadores_por_juego(game_id):
    conn = sqlite3.connect('bolera.db')
    cursor = conn.cursor()

    cursor.execute('''
        SELECT player_name, score, photo_path
        FROM jugadores_por_juego
        WHERE game_id = ?
    ''', (game_id,))

    jugadores = cursor.fetchall()
    conn.close()
    return jugadores

def actualizar_foto_jugador(game_id, player_name, photo_path):
    conn = sqlite3.connect('bolera.db')
    cursor = conn.cursor()

    cursor.execute('''
        UPDATE jugadores_por_juego
        SET photo_path = ?
        WHERE game_id = ? AND player_name = ?
    ''', (photo_path, game_id, player_name))

    conn.commit()
    conn.close()

def abrir_todas_las_pistas():
    conn = sqlite3.connect('bolera.db')
    cursor = conn.cursor()
    num_pistas = 8  # Asumimos que tienes 8 pistas

    print("Intentando encender las computadoras de las pistas...")
    pistas_listas = {}
    todas_listas = True

    for i in range(1, num_pistas + 1):
        # Simulación de enviar comando y esperar respuesta
        print("Enviando comando de encendido a la pista {}...".format(i))
        time.sleep(1)  # Simula un pequeño retraso

        # Simulación de la respuesta (podríamos hacerlo aleatorio en una simulación más compleja)
        respuesta = True  # Por ahora, simulamos que todas responden OK
        if respuesta:
            print("La computadora de la pista {} respondió: LISTA.".format(i))
            pistas_listas[i] = 'disponible'
        else:
            print("Error: La computadora de la pista {} no respondió o reportó un problema.".format(i))
            pistas_listas[i] = 'fuera de servicio'
            todas_listas = False

    if todas_listas:
        try:
            # Actualizar el estado de todas las pistas a 'disponible' en la base de datos
            cursor.execute("UPDATE pistas SET estado = 'disponible'")
            conn.commit()
            print("Todas las pistas han sido marcadas como disponibles en la base de datos.")
        except sqlite3.Error as e:
            print("Error al actualizar el estado de las pistas en la base de datos:", e)
            conn.rollback()
        finally:
            conn.close()
            return True
    else:
        print("No todas las computadoras de las pistas están listas. No se actualizará el estado en la base de datos.")
        conn.close()
        return False

# if __name__ == "__main__":
    # ... (resto de la sección if __name__ == "__main__": si la tienes)
    # pass