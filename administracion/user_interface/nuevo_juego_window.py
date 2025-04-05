print("¡¡¡NUEVO_JUEGO_WINDOW.PY HA SIDO IMPORTADO!!!")
import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
import datetime

PRECIO_POR_JUEGO = 5.00
PRECIO_POR_ZAPATOS = 2.00

def mostrar_nuevo_juego_window(root, lane_number=None):
    nuevo_juego_ventana = tk.Toplevel(root)
    nuevo_juego_ventana.title("Crear Nuevo Juego")

    # Número de Pista
    lbl_pista = ttk.Label(nuevo_juego_ventana, text="Pista:")
    lbl_pista.grid(row=0, column=0, padx=5, pady=5, sticky="w")
    num_pista_var = tk.StringVar()
    if lane_number:
        num_pista_var.set(str(lane_number))
    spn_pista = ttk.Spinbox(nuevo_juego_ventana, from_=1, to=8, width=5, textvariable=num_pista_var, state='readonly')
    spn_pista.grid(row=0, column=1, padx=5, pady=5, sticky="e")

    # Hora de Inicio
    lbl_hora_inicio = ttk.Label(nuevo_juego_ventana, text="Hora Inicio:")
    lbl_hora_inicio.grid(row=1, column=0, padx=5, pady=5, sticky="w")
    hora_inicio_var = tk.StringVar(value=datetime.datetime.now().strftime("%H:%M:%S"))
    ent_hora_inicio = ttk.Entry(nuevo_juego_ventana, textvariable=hora_inicio_var, state='readonly', width=8)
    ent_hora_inicio.grid(row=1, column=1, padx=5, pady=5, sticky="e")

    # Número de Jugadores
    lbl_num_jugadores = ttk.Label(nuevo_juego_ventana, text="Jugadores:")
    lbl_num_jugadores.grid(row=2, column=0, padx=5, pady=5, sticky="w")
    num_jugadores_var = tk.IntVar(value=1)
    spn_num_jugadores = ttk.Spinbox(nuevo_juego_ventana, from_=1, to=6, width=5, textvariable=num_jugadores_var)
    spn_num_jugadores.grid(row=2, column=1, padx=5, pady=5, sticky="e")

    # Juegos Vendidos
    lbl_juegos = ttk.Label(nuevo_juego_ventana, text="Juegos Vendidos:")
    lbl_juegos.grid(row=3, column=0, padx=5, pady=5, sticky="w")
    juegos_vendidos_var = tk.IntVar(value=1)
    spn_juegos = ttk.Spinbox(nuevo_juego_ventana, from_=0, width=5, textvariable=juegos_vendidos_var, command=lambda: calcular_total())
    spn_juegos.grid(row=3, column=1, padx=5, pady=5, sticky="e")
    juegos_vendidos_var.trace_add("write", lambda name, index, mode, sv=juegos_vendidos_var: calcular_total())

    # Zapatos Rentados
    lbl_zapatos = ttk.Label(nuevo_juego_ventana, text="Zapatos Rentados:")
    lbl_zapatos.grid(row=4, column=0, padx=5, pady=5, sticky="w")
    zapatos_rentados_var = tk.IntVar(value=0)
    spn_zapatos = ttk.Spinbox(nuevo_juego_ventana, from_=0, width=5, textvariable=zapatos_rentados_var, command=lambda: calcular_total())
    spn_zapatos.grid(row=4, column=1, padx=5, pady=5, sticky="e")
    zapatos_rentados_var.trace_add("write", lambda name, index, mode, sv=zapatos_rentados_var: calcular_total())

    # Descuento (%)
    lbl_descuento = ttk.Label(nuevo_juego_ventana, text="Descuento (%):")
    lbl_descuento.grid(row=5, column=0, padx=5, pady=5, sticky="w")
    descuento_var = tk.DoubleVar(value=0.0)
    ent_descuento = ttk.Entry(nuevo_juego_ventana, width=5, textvariable=descuento_var)
    ent_descuento.grid(row=5, column=1, padx=5, pady=5, sticky="e")
    descuento_var.trace_add("write", lambda name, index, mode, sv=descuento_var: calcular_total())

    # Total a Pagar
    lbl_total = ttk.Label(nuevo_juego_ventana, text="Total a Pagar:")
    lbl_total.grid(row=6, column=0, padx=5, pady=5, sticky="w")
    total_pagar_var = tk.StringVar(value=f"{0.00:.2f}")
    ent_total = ttk.Entry(nuevo_juego_ventana, textvariable=total_pagar_var, state='readonly', width=8)
    ent_total.grid(row=6, column=1, padx=5, pady=5, sticky="e")

    # Cantidad Recibida
    lbl_recibido = ttk.Label(nuevo_juego_ventana, text="Cantidad Recibida:")
    lbl_recibido.grid(row=7, column=0, padx=5, pady=5, sticky="w")
    cantidad_recibida_var = tk.DoubleVar(value=0.0)
    ent_recibido = ttk.Entry(nuevo_juego_ventana, width=8, textvariable=cantidad_recibida_var)
    ent_recibido.grid(row=7, column=1, padx=5, pady=5, sticky="e")
    cantidad_recibida_var.trace_add("write", lambda name, index, mode, sv=cantidad_recibida_var: calcular_cambio())

    # Cambio
    lbl_cambio = ttk.Label(nuevo_juego_ventana, text="Cambio:")
    lbl_cambio.grid(row=8, column=0, padx=5, pady=5, sticky="w")
    cambio_var = tk.StringVar(value=f"{0.00:.2f}")
    ent_cambio = ttk.Entry(nuevo_juego_ventana, textvariable=cambio_var, state='readonly', width=8)
    ent_cambio.grid(row=8, column=1, padx=5, pady=5, sticky="e")

    def calcular_total():
        try:
            num_juegos = juegos_vendidos_var.get()
            num_zapatos = zapatos_rentados_var.get()
            descuento = descuento_var.get()
            total = (num_juegos * PRECIO_POR_JUEGO) + (num_zapatos * PRECIO_POR_ZAPATOS)
            total_con_descuento = total * (1 - descuento / 100)
            total_pagar_var.set(f"{total_con_descuento:.2f}")
            calcular_cambio() # Recalcular el cambio al cambiar el total
        except ValueError:
            total_pagar_var.set("Error")

    def calcular_cambio():
        try:
            total_pagar = float(total_pagar_var.get())
            cantidad_recibida = cantidad_recibida_var.get()
            cambio = cantidad_recibida - total_pagar
            cambio_var.set(f"{cambio:.2f}")
        except ValueError:
            cambio_var.set("Error")

    # Botones
    btn_comenzar = ttk.Button(nuevo_juego_ventana, text="Comenzar Juego", command=lambda: print("Juego comenzado"))
    btn_comenzar.grid(row=9, column=0, columnspan=2, padx=5, pady=10)

    btn_cancelar = ttk.Button(nuevo_juego_ventana, text="Cancelar", command=nuevo_juego_ventana.destroy)
    btn_cancelar.grid(row=10, column=0, columnspan=2, padx=5, pady=5)