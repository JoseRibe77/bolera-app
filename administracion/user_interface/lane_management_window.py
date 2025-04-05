import tkinter as tk
import time
import datetime
from administracion.user_interface.configuracion_window import ConfiguracionWindow # type: ignore
from PIL import Image, ImageTk

class LaneManagementWindow(tk.Toplevel):
    def __init__(self, parent=None, bg_color=None):
        super().__init__(parent)
        self.title("Administración de Pistas")
        self.geometry("1200x700")
        self.parent = parent
        self.bg_color = bg_color
        self.main_window = parent
        self.botones_categoria = {}
        self.botones_activos = None
        self._build_ui()

    def _build_ui(self):
        self._build_top_section()
        self.left_frame = tk.Frame(self)
        self.left_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=10, pady=10)

        self.right_frame = tk.Frame(self)
        self.right_frame.pack(side=tk.RIGHT, fill=tk.Y, padx=10)

        self._build_lane_display()
        self._build_collapsible_buttons()

        self._update_datetime()
        self._actualizar_textos_idioma() # Llamar a la función para actualizar el idioma después de construir la UI

    def _cargar_configuracion(self):
        import os
        import json
        ruta_archivo = os.path.join(os.path.dirname(__file__), 'config.json')
        try:
            with open(ruta_archivo, 'r') as f:
                configuracion = json.load(f)
                return configuracion
        except FileNotFoundError:
            print("Error: El archivo config.json no se encontró.")
            return {}
        except json.JSONDecodeError:
            print("Error: El archivo config.json tiene un formato incorrecto.")
            return {}

    def _build_top_section(self):
        top_frame = tk.Frame(self, height=50, bg='#f0f0f0')
        top_frame.pack(side=tk.TOP, fill=tk.X)

        # Título del software
        # title_label = tk.Label(top_frame, text="PeRa's Bowling System", font=("Arial", 16), bg='#f0f0f0')
        # title_label.pack(side=tk.LEFT, padx=10, pady=10)

        # Logo
        try:
            image = Image.open("administracion/imagenes/usuarios/bolo-logo.png")
            image = image.resize((300, 100))
            self.logo_image = ImageTk.PhotoImage(image)
            logo_label = tk.Label(top_frame, image=self.logo_image, bg='#f0f0f0')
            logo_label.pack(side=tk.LEFT, padx=10, pady=10)
        except FileNotFoundError:
            logo_label = tk.Label(top_frame, text="[Logo]", font=("Arial", 12), bg='#f0f0f0')
            logo_label.pack(side=tk.LEFT, padx=10, pady=10)

        # Información para el operador
        self.info_label = tk.Label(top_frame, text="Información para el operador...", bg='#f0f0f0')
        self.info_label.pack(side=tk.LEFT, padx=10, pady=10)

        # Fecha y hora
        self.date_label = tk.Label(top_frame, text="", font=("Arial", 12), bg='#f0f0f0')
        self.date_label.pack(side=tk.RIGHT, padx=10, pady=10)

        self.time_label = tk.Label(top_frame, text="", font=("Arial", 12), bg='#f0f0f0')
        self.time_label.pack(side=tk.RIGHT, padx=10, pady=10)

    def _update_datetime(self):
        now = datetime.datetime.now()
        current_time = now.strftime("%H:%M:%S")
        current_date = now.strftime("%Y-%m-%d")
        self.time_label.config(text=current_time)
        self.date_label.config(text=current_date)
        self.after(1000, self._update_datetime)

    def _build_lane_display(self):
        # Sección de estado de las pistas
        status_frame = tk.LabelFrame(self.left_frame, text="Estado de Pistas", padx=10, pady=10)
        status_frame.pack(fill=tk.X, pady=10)

        available_label = tk.Label(status_frame, text="Pista Disponible", bg='green', fg='white', padx=10, pady=5)
        available_label.pack(side=tk.LEFT, padx=5)

        busy_label = tk.Label(status_frame, text="Pista Ocupada", bg='red', fg='white', padx=10, pady=5)
        busy_label.pack(side=tk.LEFT, padx=5)

        disabled_label = tk.Label(status_frame, text="Pista Deshabilitada", bg='gray', fg='white', padx=10, pady=5)
        disabled_label.pack(side=tk.LEFT, padx=5)

        # Sección de visualización de pistas
        lanes_frame = tk.Frame(self.left_frame)
        lanes_frame.pack(fill=tk.BOTH, expand=True)

        self.lane_states = {} # Diccionario para almacenar el estado de cada pista
        self.lane_buttons = {} # Diccionario para almacenar los botones de cada pista

        configuracion = self._cargar_configuracion()
        num_lanes = configuracion.get('numero_de_pistas', 6) # Lee el número de pistas, usa 6 si no se encuentra

        lanes_per_row = 6
        for i in range(1, num_lanes + 1):
            nombre_pista = f"Pista {i}"
            lane_button = tk.Button(lanes_frame, text=nombre_pista + "\nDisponible", width=8, height=3,
                                     command=lambda pista=nombre_pista: self._cambiar_estado_pista(pista),
                                     bg='green') # Añadimos el color de fondo inicial
            self.lane_states[nombre_pista] = "Disponible" # Guardamos el estado inicial
            self.lane_buttons[nombre_pista] = lane_button # Guardamos el botón

            row = (i - 1) // lanes_per_row
            col = (i - 1) % lanes_per_row
            lane_button.grid(row=row, column=col, padx=5, pady=5)

    def _build_collapsible_buttons(self):
        # Botones principales
        self.generales_button = tk.Button(self.right_frame, text="Generales", width=15, bg="lightblue", command=lambda: self._mostrar_botones('generales'))
        self.generales_button.pack(pady=5)

        self.opciones_pista_button = tk.Button(self.right_frame, text="Opciones de Pista", width=15, bg="lightblue", command=lambda: self._mostrar_botones('pista'))
        self.opciones_pista_button.pack(pady=5)

        self.opciones_usuario_button = tk.Button(self.right_frame, text="Opciones de Usuario", width=15, bg="lightblue", command=lambda: self._mostrar_botones('usuario'))
        self.opciones_usuario_button.pack(pady=5)

        self.opciones_button = tk.Button(self.right_frame, text="Opciones", width=15, bg="lightblue", command=lambda: self._mostrar_botones('opciones'))
        self.opciones_button.pack(pady=5)

        # Frames para los botones secundarios
        self.generales_frame = None
        self.opciones_pista_frame = None
        self.opciones_usuario_frame = None
        self.opciones_frame_bottom = None

        self.botones_activos = None

    def _mostrar_botones(self, categoria):
        if self.botones_activos:
            self.botones_activos.pack_forget()
            self.botones_activos = None

        if categoria == 'generales':
            if not self.generales_frame:
                self.generales_frame = tk.Frame(self.right_frame)
                tk.Button(self.generales_frame, text="Ajustes", width=15, bg="lightgray").pack(pady=2)
                tk.Button(self.generales_frame, text="Turno", width=15, bg="lightgray").pack(pady=2)
                tk.Button(self.generales_frame, text="Reportes", width=15, bg="lightgray").pack(pady=2)
                tk.Button(self.generales_frame, text="Billar", width=15, bg="lightgray").pack(pady=2)
                tk.Button(self.generales_frame, text="Comidas/Bebidas", width=15, bg="lightgray").pack(pady=2)
                tk.Button(self.generales_frame, text="Cuentas", width=15, bg="lightgray").pack(pady=2)
                tk.Button(self.generales_frame, text="Renta se Zapatillas", width=15, bg="lightgray").pack(pady=2)
                tk.Button(self.generales_frame, text="Stock", width=15, bg="lightgray").pack(pady=2)
                tk.Button(self.generales_frame, text="Ayuda", width=15, bg="lightgray").pack(pady=2)
            self.generales_frame.pack(pady=5, after=self.generales_button)
            self.botones_activos = self.generales_frame
        elif categoria == 'pista':
            if not self.opciones_pista_frame:
                self.opciones_pista_frame = tk.Frame(self.right_frame)
                tk.Button(self.opciones_pista_frame, text="Abrir Juego", width=15, bg="lightgray").pack(pady=2)
                tk.Button(self.opciones_pista_frame, text="Juego Anterior", width=15, bg="lightgray").pack(pady=2)
                tk.Button(self.opciones_pista_frame, text="Actualizar Estado", width=15, bg="lightgray").pack(pady=2)
                tk.Button(self.opciones_pista_frame, text="Repetir Juego", width=15, bg="lightgray").pack(pady=2)
                tk.Button(self.opciones_pista_frame, text="Juego de Prueba", width=15, bg="lightgray").pack(pady=2)
                tk.Button(self.opciones_pista_frame, text="Cancelar", width=15, bg="lightgray").pack(pady=2)
                tk.Button(self.opciones_pista_frame, text="Enviar Mensaje", width=15, bg="lightgray").pack(pady=2)
                tk.Button(self.opciones_pista_frame, text="Puntuaciones", width=15, bg="lightgray").pack(pady=2)
                tk.Button(self.opciones_pista_frame, text="Actualizar juego transferido", width=15, bg="lightgray").pack(pady=2)
                tk.Button(self.opciones_pista_frame, text="Control de Tiempo", width=15, bg="lightgray").pack(pady=2)
                tk.Button(self.opciones_pista_frame, text="Imprimir Juego", width=15, bg="lightgray").pack(pady=2)
                tk.Button(self.opciones_pista_frame, text="Restaurar Juego", width=15, bg="lightgray").pack(pady=2)
            self.opciones_pista_frame.pack(pady=5, after=self.opciones_pista_button)
            self.botones_activos = self.opciones_pista_frame
        elif categoria == 'usuario':
            if not self.opciones_usuario_frame:
                self.opciones_usuario_frame = tk.Frame(self.right_frame)
                tk.Button(self.opciones_usuario_frame, text="Cambiar Contraseña", width=15, bg="lightgray").pack(pady=2)
                tk.Button(self.opciones_usuario_frame, text="Cerrar Sesión", width=15, command=self._cerrar_sesion, bg="lightgray").pack(pady=2) # Cambiamos la función a _cerrar_sesion
                tk.Button(self.opciones_usuario_frame, text="Salir del Programa", width=15, command=self._cerrar_aplicacion, bg="lightgray").pack(pady=2) # Añadimos el nuevo botón
                tk.Button(self.opciones_usuario_frame, text="Otros", width=15, bg="lightgray").pack(pady=2)
                tk.Button(self.opciones_usuario_frame, text="Opciones de Admin", width=15, bg="lightgray").pack(pady=2)
            self.opciones_usuario_frame.pack(pady=5, after=self.opciones_usuario_button)
            self.botones_activos = self.opciones_usuario_frame
        elif categoria == 'opciones':
            if not self.opciones_frame_bottom:
                self.opciones_frame_bottom = tk.Frame(self.right_frame)
                tk.Button(self.opciones_frame_bottom, text="Promociones", width=15, bg="lightgray").pack(pady=2)
                tk.Button(self.opciones_frame_bottom, text="Jugadores", width=15, bg="lightgray").pack(pady=2)
                tk.Button(self.opciones_frame_bottom, text="Mejores Jugadores", width=15, bg="lightgray").pack(pady=2)
                tk.Button(self.opciones_frame_bottom, text="Abrir Turno", width=15, bg="lightgray").pack(pady=2)
                tk.Button(self.opciones_frame_bottom, text="Estado del Turno", width=15, bg="lightgray").pack(pady=2)
                tk.Button(self.opciones_frame_bottom, text="Usuarios", width=15, bg="lightgray").pack(pady=2)
                tk.Button(self.opciones_frame_bottom, text="Opciones", width=15, bg="lightgray", command=self._mostrar_ventana_configuracion).pack(pady=2) # Añade este botón
                tk.Button(self.opciones_frame_bottom, text="Salir", width=15, command=self._cerrar_aplicacion, bg="lightgray").pack(pady=2)

                # tk.Button(self.opciones_frame_bottom, text="Abrir Caja", width=15, bg="lightgray").pack(pady=2)
                # tk.Button(self.opciones_frame_bottom, text="Ligas", width=15, bg="lightgray").pack(pady=2)
                # tk.Button(self.opciones_frame_bottom, text="Lista de Espera", width=15, bg="lightgray").pack(pady=2)
                # tk.Button(self.opciones_frame_bottom, text="Cerrar Turno", width=15, bg="lightgray").pack(pady=2)
                # tk.Button(self.opciones_frame_bottom, text="Turno Cerrado", width=15, bg="lightgray").pack(pady=2)
                # tk.Button(self.opciones_frame_bottom, text="Estatus Pistas", width=15, bg="lightgray").pack(pady=2)
                # tk.Button(self.opciones_frame_bottom, text="Diseño de Documentos", width=15, bg="lightgray").pack(pady=2)
                # tk.Button(self.opciones_frame_bottom, text="ShutDown", width=15, bg="lightgray").pack(pady=2)
            self.opciones_frame_bottom.pack(pady=5, after=self.opciones_button)
            self.botones_activos = self.opciones_frame_bottom

    def _cerrar_sesion(self):
        self.destroy() # Cierra la ventana de administración de pistas
        if self.parent:
            self.parent._mostrar_login() # Llama al método en MainWindow para mostrar la ventana de login

    def _mostrar_ventana_configuracion(self):
        if self.main_window: # Asegurarnos de que main_window está definido
            ConfiguracionWindow(self.main_window, on_config_save=self._actualizar_configuracion_main)

    def _actualizar_configuracion_main(self):
        print("_actualizar_configuracion_main llamado")
        if self.main_window:
            print(f"Idioma en MainWindow ANTES de recargar: {self.main_window.configuracion.get('idioma')}") # Nueva línea
            print("self.main_window existe")
            self.main_window._cargar_configuracion()
            print(f"Idioma en MainWindow DESPUÉS de la primera carga en _actualizar: {self.main_window.configuracion.get('idioma')}")
            self.main_window._cargar_traducciones()
            print(f"Idioma en MainWindow DESPUÉS de recargar traducciones: {self.main_window.configuracion.get('idioma')}")
            self.main_window.config(bg=self.main_window.configuracion.get('color_fondo', 'SystemButtonFace'))
            self.config(bg=self.main_window.configuracion.get('color_fondo', 'SystemButtonFace'))
            self._actualizar_textos_idioma()
    
    def _actualizar_textos_idioma(self):
        print("_actualizar_textos_idioma llamado")
        idioma_actual = self.main_window.configuracion.get('idioma', 'es') # Mantenemos esta línea para el log
        print(f"Idioma actual (antes de usarlo para la traducción): {idioma_actual}")
        idioma_para_traduccion = self.main_window.configuracion.get('idioma') # Accedemos directamente al idioma
        self.title(self.main_window.get_translation('lane_management_title'))
        print(f"Título actualizado a: {self.title()}")
        self.generales_button.config(text=self.main_window.get_translation('generales_button_text') or "Generales")
        self.opciones_pista_button.config(text=self.main_window.get_translation('opciones_pista_button_text') or "Opciones de Pista")
        self.opciones_usuario_button.config(text=self.main_window.get_translation('opciones_usuario_button_text') or "Opciones de Usuario")
        self.opciones_button.config(text=self.main_window.get_translation('opciones_button_text') or "Opciones")

    def _cargar_configuracion(self):
        import os
        import json
        ruta_archivo = os.path.join(os.path.dirname(__file__), 'config.json')
        try:
            with open(ruta_archivo, 'r') as f:
                configuracion = json.load(f)
                return configuracion
        except FileNotFoundError:
            print("Error: El archivo config.json no se encontró.")
            return {}
        except json.JSONDecodeError:
            print("Error: El archivo config.json tiene un formato incorrecto.")
            return {}

    def _cambiar_estado_pista(self, nombre_pista):
        estados = ["Disponible", "Ocupada", "Deshabilitada"]
        colores = {"Disponible": "green", "Ocupada": "red", "Deshabilitada": "gray"}
        estado_actual = self.lane_states.get(nombre_pista)

        if estado_actual in estados:
            indice_actual = estados.index(estado_actual)
            siguiente_indice = (indice_actual + 1) % len(estados)
            nuevo_estado = estados[siguiente_indice]
            self.lane_states[nombre_pista] = nuevo_estado

            # Actualizar el texto y el color del botón
            boton = self.lane_buttons.get(nombre_pista)
            if boton:
                boton.config(text=f"{nombre_pista}\n{nuevo_estado}", bg=colores.get(nuevo_estado, "white"))
        else:
            # Si el estado actual no es reconocido, lo inicializamos a Disponible
            self.lane_states[nombre_pista] = "Disponible"
            boton = self.lane_buttons.get(nombre_pista)
            if boton:
                boton.config(text=f"{nombre_pista}\nDisponible", bg="green")

    def _cerrar_aplicacion(self):
        if self.parent: # Estamos usando self.parent en lugar de self.main_window
            self.parent._on_closing()
        self.destroy() # Esto cierra la ventana de pistas

if __name__ == '__main__':
    app = LaneManagementWindow()
    app.mainloop()