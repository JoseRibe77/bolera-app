import tkinter as tk
from administracion.user_interface import login_window
from administracion.user_interface import nuevo_juego_window
from administracion.user_interface import lane_management_window
import json
import os

class MainWindow(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Bolera App")
        self.attributes('-fullscreen', True) # Vamos a dejar esto comentado por ahora
        self.configuracion = self._cargar_configuracion() # Cargar la configuración al inicio
        self.translations = self._cargar_traducciones() # Cargar las traducciones
        self.config(bg=self.configuracion.get('color_fondo', 'SystemButtonFace')) # Establecer color de fondo de la ventana principal
        self._mostrar_login()
    
    def _cargar_traducciones(self):
        import json
        import os
        ruta_archivo = os.path.join(os.path.dirname(__file__), 'translations.json')
        try:
            with open(ruta_archivo, 'r', encoding='utf-8') as f:
                traducciones = json.load(f)
                print(f"Traducciones cargadas: {traducciones}")
                return traducciones
        except FileNotFoundError:
            print("Error: El archivo translations.json no se encontró.")
            return {}
        except json.JSONDecodeError:
            print("Error: El archivo translations.json tiene un formato incorrecto.")
            return {}

    def get_translation(self, key):
        idioma = self.configuracion.get('idioma', 'es') # Obtener el idioma de la configuración
        return self.translations.get(key, {}).get(idioma, key) # Devolver la traducción o la clave si no se encuentra

    def _cargar_configuracion(self):
        import json
        import os
        ruta_archivo = os.path.join(os.path.dirname(__file__), 'user_interface', 'config.json')
        print(f"Intentando cargar configuración desde: {ruta_archivo}")
        try:
            with open(ruta_archivo, 'r', encoding='utf-8') as f:
                raw_content = f.read()
                print(f"Contenido del archivo de configuración: {raw_content}")
                loaded_config = json.loads(raw_content)
                print(f"MainWindow loaded config: {loaded_config}")
                if hasattr(self, 'configuracion') and isinstance(self.configuracion, dict):
                    self.configuracion.clear() # Limpiar el diccionario existente
                    self.configuracion.update(loaded_config) # Actualizar con los nuevos valores
                else:
                    self.configuracion = loaded_config # Si no existe, crear uno nuevo
                return self.configuracion
        except FileNotFoundError:
            print("Error: El archivo config.json no se encontró.")
            return {}
        except json.JSONDecodeError:
            print("Error: El archivo config.json tiene un formato incorrecto.")
            return {}

    def _mostrar_login(self):
        if hasattr(self, 'login_window') and self.login_window:
            self.login_window.destroy()
            self.login_window = None
        config = self._cargar_configuracion() # Cargar la configuración
        self.translations = self._cargar_traducciones() # Recargar las traducciones
        bg_color = config.get('color_fondo', 'SystemButtonFace')
        self.config(bg=bg_color) # Forzar la actualización del fondo de MainWindow
        self.update() # Forzar un redibujo inmediato de MainWindow
        self.login_window = login_window.LoginWindow(self, on_login_success=self._handle_inicio_sesion_exitoso, configuracion=config) # Pasar la configuración cargada
        self.withdraw() # Ocultar la ventana principal

    def _handle_inicio_sesion_exitoso(self):
        self._mostrar_lane_management()

    def _mostrar_lane_management(self):
        self.lane_management_window = lane_management_window.LaneManagementWindow(self, self.configuracion.get('color_fondo')) # Pasar el color de fondo
        self.login_window.destroy()

    def _mostrar_nuevo_juego(self):
        nuevo_juego_window.NuevoJuegoWindow(self)
    
    def _on_closing(self):
        self.destroy() # Esto cierra la ventana principal y la aplicación

if __name__ == '__main__':
    app = MainWindow()
    app.mainloop()