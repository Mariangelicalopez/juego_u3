# ventanas/ventana_configuracion.py
import tkinter as tk
from tkinter import messagebox
from ventanas.ventana_juego import JuegoAdivinanzaInteractivo

class VentanaConfiguracion:
    def __init__(self, master):
        self.master = master
        self.master.title("Configuración del Juego")
        self.master.geometry("350x220")
        self.master.resizable(False, False)

        self.fuente_normal = ("Arial", 12)
        self.color_boton = "#2e7d32"  # Verde

        frame = tk.Frame(master, padx=20, pady=20)
        frame.pack(fill="both", expand=True)

        # Etiquetas y entradas para rango mínimo y máximo
        tk.Label(frame, text="Elige el rango de números:", font=self.fuente_normal).pack(anchor="w")
        rango_frame = tk.Frame(frame)
        rango_frame.pack(pady=(0, 15), fill="x")

        self.entry_min = tk.Entry(rango_frame, width=8, font=self.fuente_normal)
        self.entry_min.insert(0, "1")
        self.entry_min.pack(side="left", padx=(0, 10))

        self.entry_max = tk.Entry(rango_frame, width=8, font=self.fuente_normal)
        self.entry_max.insert(0, "100")
        self.entry_max.pack(side="left")

        # Entrada para número de intentos
        tk.Label(frame, text="Número de intentos:", font=self.fuente_normal).pack(anchor="w")
        self.entry_intentos = tk.Entry(frame, width=8, font=self.fuente_normal)
        self.entry_intentos.insert(0, "10")
        self.entry_intentos.pack(pady=(0, 15), anchor="w")

        # Botón para iniciar el juego
        self.boton_iniciar = tk.Button(
            frame, text="Iniciar Juego", font=self.fuente_normal,
            bg=self.color_boton, fg="white", activebackground="#1b5e20",
            command=self.validar_y_abrir_juego
        )
        self.boton_iniciar.pack(fill="x")

    def validar_y_abrir_juego(self):
        """
        Valida las entradas y si son correctas, cierra esta ventana y abre la ventana del juego.
        """
        try:
            rango_min = int(self.entry_min.get())
            rango_max = int(self.entry_max.get())
            intentos_max = int(self.entry_intentos.get())
            if rango_min >= rango_max:
                messagebox.showerror("Error de rango", "El rango mínimo debe ser menor que el máximo.")
                return
            if intentos_max <= 0:
                messagebox.showerror("Error de intentos", "El número de intentos debe ser mayor que cero.")
                return
        except ValueError:
            messagebox.showerror("Error de entrada", "Por favor, ingresa números válidos.")
            return

        # Abrir ventana principal del juego y cerrar esta ventana
        self.master.destroy()
        root_juego = tk.Tk()
        JuegoAdivinanzaInteractivo(root_juego, rango_min, rango_max, intentos_max)
        root_juego.mainloop()
