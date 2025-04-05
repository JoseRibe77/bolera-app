import tkinter as tk
from tkinter import messagebox
import hashlib
import os
import json
from PIL import Image, ImageTk

USUARIOS_SEGUROS_FILE = 'usuarios_seguros.json'

class LoginWindow(tk.Toplevel):
    def __init__(self, parent, on_login_success=None, configuracion=None):
        super().__init__(parent)
        self.parent = parent
        self.title(self.parent.get_translation('login_title')) # Establecer el título usando la traducción
        # self.attributes('-fullscreen', True)
        self.on_login_success = on_login_success
        self.usuario_seleccionado = None
        self.usuario_seleccionado_label = None
        self.configuracion = configuracion if configuracion else {} # Guardar la configuración
        print(f"LoginWindow received config: {self.configuracion}") # Ahora esto funcionará
        self._build_ui()

    def _build_ui(self):
        bg_color = self.configuracion.get('color_fondo', 'SystemButtonFace') # Obtener el color de fondo o usar uno por defecto
        self.config(bg=bg_color) # Establecer el color de fondo de la ventana

        frame_seleccion_usuario = tk.Frame(self, bg=bg_color) # Asegúrate de que los frames también tengan el mismo color de fondo
        frame_seleccion_usuario.pack(pady=10)

        self.usuario_seleccionado_label = tk.Label(frame_seleccion_usuario, text="", font=("Arial", 12), bg=bg_color)
        self.usuario_seleccionado_label.pack()

        # Logo
        try:
            image = Image.open("administracion/imagenes/usuarios/bolo-logo.png")
            image = image.resize((300, 100))
            self.logo_image = ImageTk.PhotoImage(image)
            logo_label = tk.Label(frame_seleccion_usuario, image=self.logo_image, bg=bg_color)
            logo_label.pack(side=tk.LEFT, padx=10, pady=10)
        except FileNotFoundError:
            logo_label = tk.Label(frame_seleccion_usuario, text="[Logo]", font=("Arial", 12), bg=bg_color)
            logo_label.pack(side=tk.LEFT, padx=10, pady=10)

        label_titulo = tk.Label(self, text="Seleccione un usuario para iniciar sesión", font=("Arial", 16), bg=bg_color)
        label_titulo.pack(pady=20)

        frame_usuarios = tk.Frame(self, bg=bg_color)
        frame_usuarios.pack(pady=10)

        usuarios_seguros = self._cargar_usuarios()
        self.botones_usuario = {} # Inicializamos el diccionario para guardar los botones de usuario
        button_size = 90 # Ajusta este valor para cambiar el tamaño aproximado

        for nombre, detalles in usuarios_seguros.items():
            imagen_tk = self._cargar_imagen(nombre)
            if imagen_tk:
                boton_usuario = tk.Button(frame_usuarios, image=imagen_tk, width=button_size, height=button_size,
                                         command=lambda n=nombre: self._seleccionar_usuario(n))
                boton_usuario.image = imagen_tk
                boton_usuario.pack(side=tk.LEFT, padx=10)
            else:
                boton_usuario = tk.Button(frame_usuarios, text=nombre, width=button_size, height=button_size,
                                         command=lambda n=nombre: self._seleccionar_usuario(n))
                boton_usuario.pack(side=tk.LEFT, padx=10)
            self.botones_usuario[nombre] = boton_usuario # Guardamos el botón en el diccionario

        label_password = tk.Label(self, text="Contraseña:", font=("Arial", 12), bg=bg_color)
        label_password.pack(pady=10)

        self.entry_password = tk.Entry(self, show="*", font=("Arial", 12))
        self.entry_password.pack(pady=5)

        button_login = tk.Button(self, text="Iniciar Sesión", command=self._iniciar_sesion, font=("Arial", 12))
        button_login.pack(pady=20)

    def _cargar_imagen(self, nombre_usuario):
        try:
            ruta_imagen = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'imagenes', 'usuarios', f'{nombre_usuario.lower()}.png')
            imagen = tk.PhotoImage(file=ruta_imagen)
            return imagen
        except tk.TclError:
            return None

    def _cargar_usuarios(self):
        try:
            ruta_archivo = os.path.join(os.path.dirname(__file__), USUARIOS_SEGUROS_FILE)
            with open(ruta_archivo, 'r') as f:
                usuarios = json.load(f)
            return usuarios
        except FileNotFoundError:
            return {}

    def _verificar_password(self, password_ingresado, sal_hex, hash_almacenado):
        sal = bytes.fromhex(sal_hex)
        password_hasheado = hashlib.pbkdf2_hmac('sha256', password_ingresado.encode('utf-8'), sal, 100000)
        password_hasheado_hex = password_hasheado.hex()
        return password_hasheado_hex == hash_almacenado

    def _seleccionar_usuario(self, nombre_usuario):
        color_seleccionado = "lightblue"
        color_original = "SystemButtonFace" # Color de fondo por defecto de los botones

        if self.usuario_seleccionado and self.usuario_seleccionado in self.botones_usuario:
            # Restablecer el color de fondo del botón previamente seleccionado
            boton_anterior = self.botones_usuario[self.usuario_seleccionado]
            boton_anterior.config(bg=color_original)

        self.usuario_seleccionado = nombre_usuario
        self.usuario_seleccionado_label.config(text=f"Usuario seleccionado: {nombre_usuario}")

        if self.usuario_seleccionado in self.botones_usuario:
            # Cambiar el color de fondo del botón actual
            boton_actual = self.botones_usuario[self.usuario_seleccionado]
            boton_actual.config(bg=color_seleccionado)

    def _iniciar_sesion(self):
        password_ingresado = self.entry_password.get()

        if self.usuario_seleccionado:
            usuarios_seguros = self._cargar_usuarios()
            detalles_usuario = usuarios_seguros.get(self.usuario_seleccionado)
            if detalles_usuario:
                sal_hex = detalles_usuario.get('sal')
                hash_almacenado = detalles_usuario.get('hash')
                if sal_hex and hash_almacenado:
                    if self._verificar_password(password_ingresado, sal_hex, hash_almacenado):
                        messagebox.showinfo("Inicio de Sesión", f"Inicio de sesión exitoso para {self.usuario_seleccionado}")
                        self.destroy()
                        if self.on_login_success:
                            self.on_login_success()
                    else:
                        messagebox.showerror("Error de Inicio de Sesión", "Contraseña incorrecta.")
                else:
                    messagebox.showerror("Error de Inicio de Sesión", "Error al cargar la información del usuario.")
            else:
                messagebox.showerror("Error de Inicio de Sesión", f"No se encontró información para el usuario: {self.usuario_seleccionado}")
        else:
            messagebox.showerror("Error de Inicio de Sesión", "Por favor, seleccione un usuario.")

def mostrar_login_window(root, on_login_success=None):
    LoginWindow(root, on_login_success)

if __name__ == '__main__':
    root = tk.Tk()
    root.withdraw()
    LoginWindow(root)
    root.mainloop()