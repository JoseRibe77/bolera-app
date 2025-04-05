# administracion/user_interface/main_window.py
import tkinter as tk
from tkinter import ttk
from administracion.database_management import database_handler
from administracion.user_interface import nuevo_juego_window
from administracion.user_interface import lane_management_window
from tkinter import messagebox

print("¡¡¡MAIN_WINDOW.PY HA SIDO IMPORTADO!!!")

root_window = None
buttons_to_enable = []
bolera_abierta = False # Track the state of the bolera

def abrir_bolera_interna():
    global bolera_abierta
    resultado = database_handler.abrir_todas_las_pistas()
    if resultado:
        bolera_abierta = True
        messagebox.showinfo("Bolera Abierta", "La bolera ha sido abierta y todas las pistas están disponibles.")
        return True
    else:
        messagebox.showerror("Error al Abrir", "No todas las pistas pudieron ser activadas. Consulta la terminal para más detalles.")
        return False