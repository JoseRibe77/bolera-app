import tkinter as tk
from tkinter import ttk
from tkinter import colorchooser, messagebox
import json
import os

class ConfiguracionWindow(tk.Toplevel):
    def __init__(self, parent=None, on_config_save=None):
        super().__init__(parent)
        self.title("Configuración")
        self.geometry("400x350") # Aumentamos un poco la altura para el nuevo elemento
        self.parent = parent
        self.on_config_save = on_config_save
        self.configuracion = self._cargar_configuracion()
        self.color_fondo = self.configuracion.get('color_fondo', 'SystemButtonFace')
        self.num_pistas_var = tk.StringVar(value=self.configuracion.get('numero_de_pistas', 6))
        self.idioma_var = tk.StringVar(value=self.configuracion.get('idioma', 'es')) # Establecemos 'es' (español) como predeterminado si no hay nada en la configuración
        self._build_ui()

    def _build_ui(self):
        # Frame para el color de fondo
        frame_fondo = tk.Frame(self)
        frame_fondo.pack(pady=10)
        tk.Label(frame_fondo, text="Color de Fondo:").pack(side=tk.LEFT)
        self.color_fondo_button = tk.Button(frame_fondo, text="Seleccionar Color", bg=self.color_fondo, command=self._seleccionar_color_fondo)
        self.color_fondo_button.pack(side=tk.LEFT, padx=10)

        # Frame para el número de pistas
        frame_pistas = tk.Frame(self)
        frame_pistas.pack(pady=10)
        tk.Label(frame_pistas, text="Número de Pistas:").pack(side=tk.LEFT)
        self.num_pistas_entry = tk.Entry(frame_pistas, width=5, textvariable=self.num_pistas_var) # Usamos la variable aquí
        self.num_pistas_entry.pack(side=tk.LEFT, padx=10)

        # Frame para la selección de idioma
        frame_idioma = tk.Frame(self)
        frame_idioma.pack(pady=10)
        tk.Label(frame_idioma, text="Idioma:").pack(side=tk.LEFT)
        idiomas_disponibles = ["es", "en", "fr"] # Puedes añadir más idiomas aquí
        self.idioma_combo = ttk.Combobox(frame_idioma, textvariable=self.idioma_var, values=idiomas_disponibles)
        self.idioma_combo.pack(side=tk.LEFT, padx=10)
        self.idioma_combo.set(self.idioma_var.get()) # Establecer el valor inicial

        # Botón para guardar la configuración
        guardar_button = tk.Button(self, text="Guardar Configuración", command=self._guardar_configuracion)
        guardar_button.pack(pady=20)

    def _seleccionar_color_fondo(self):
        color_code = colorchooser.askcolor(title="Seleccionar color de fondo")
        if color_code:
            self.color_fondo = color_code[1]
            self.color_fondo_button.config(bg=self.color_fondo)

    def _guardar_configuracion(self):
        try:
            num_pistas = int(self.num_pistas_var.get())
        except ValueError:
            messagebox.showerror("Error", "El número de pistas debe ser un entero.")
            return

        configuracion = {
            'color_fondo': self.color_fondo,
            'numero_de_pistas': num_pistas,
            'idioma': self.idioma_var.get() # Save the selected language
        }
        ruta_archivo = os.path.join(os.path.dirname(__file__), 'config.json')
        print(f"Intentando guardar la configuración en: {ruta_archivo}") # Añadimos esta línea
        try:
            with open(ruta_archivo, 'w') as f:
                json.dump(configuracion, f)
            messagebox.showinfo("Guardado", "Configuración guardada correctamente.")
            if self.on_config_save:
                print("Llamando a on_config_save") # Añade esta línea
                self.on_config_save()
            self.destroy()
        except Exception as e:
            messagebox.showerror("Error", f"Error al guardar la configuración: {e}")
            import traceback
            traceback.print_exc() # Añadimos esta línea para ver el error completo

    def _cargar_configuracion(self):
        ruta_archivo = os.path.join(os.path.dirname(__file__), 'config.json')
        try:
            with open(ruta_archivo, 'r') as f:
                configuracion = json.load(f)
                return configuracion
        except FileNotFoundError:
            return {}
        except json.JSONDecodeError:
            return {}

if __name__ == '__main__':
    app = ConfiguracionWindow()
    app.mainloop()