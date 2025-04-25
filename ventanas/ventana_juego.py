# Importamos librerías necesarias
import tkinter as tk
from tkinter import messagebox
import random
import pygame  # Librería para reproducir sonidos
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import matplotlib.pyplot as plt
from recursos.sonidos import generar_sonido_tono
import random as rnd  # Para elegir pistas aleatorias

# Definimos la clase principal del juego
class JuegoAdivinanzaInteractivo:
    def __init__(self, master, rango_min, rango_max, intentos_maximos):
        # Inicializamos variables principales
        self.master = master
        self.master.title("Juego de Adivinanza Interactivo")
        self.master.geometry("600x750")
        self.master.resizable(False, False)

        # Inicializamos sonido (pygame)
        pygame.mixer.init()

        # Generamos sonidos dinámicamente (frecuencia y duración)
        self.sonido_correcto = pygame.mixer.Sound(file=generar_sonido_tono(880, 0.3))
        self.sonido_incorrecto = pygame.mixer.Sound(file=generar_sonido_tono(440, 0.2))
        self.sonido_error = pygame.mixer.Sound(file=generar_sonido_tono(220, 0.4))


        # Configuramos variables de juego
        self.intentos = []
        self.puntaje = 0
        self.rango_min = rango_min
        self.rango_max = rango_max
        self.intentos_maximos = intentos_maximos
        self.numero_secreto = random.randint(self.rango_min, self.rango_max)

        # --- Estilos (colores, fuentes) ---
        self.fuente_titulo = ("Arial", 18, "bold")
        self.fuente_normal = ("Arial", 12)
        self.color_exito = "#2e7d32"  
        self.color_error = "#c62828"
        self.color_pista = "#ef6c00"
        self.color_boton = "#1565c0"
        self.color_boton_reintentar = "#f57c00"

        # --- Construcción de la interfaz gráfica (Widgets) ---

        # Contenedor principal
        self.frame = tk.Frame(master, padx=20, pady=20)
        self.frame.pack(fill="both", expand=True)

        # Título
        self.label_titulo = tk.Label(self.frame, text="Juego de Adivinanza", font=self.fuente_titulo)
        self.label_titulo.pack(pady=(0, 15))

        # Instrucciones
        self.label_instrucciones = tk.Label(
            self.frame,
            text=f"Adivina el número entre {self.rango_min} y {self.rango_max}. Tienes {self.intentos_maximos} intentos.",
            font=self.fuente_normal
        )
        self.label_instrucciones.pack()

        # Entrada de número
        self.entrada = tk.Entry(self.frame, font=self.fuente_normal, justify="center")
        self.entrada.pack(pady=(10, 10), fill="x")

        # Botón Adivinar
        self.boton_adivinar = tk.Button(
            self.frame, text="Adivinar", font=self.fuente_normal,
            bg=self.color_boton, fg="white", activebackground="#0d47a1",
            command=self.adivinar
        )
        self.boton_adivinar.pack(pady=(0, 20), fill="x")

        # Mensajes de resultado y pista
        self.label_resultado = tk.Label(self.frame, text="", font=self.fuente_normal, wraplength=560)
        self.label_resultado.pack(pady=(0, 10))

        self.label_pista = tk.Label(self.frame, text="", font=self.fuente_normal, fg=self.color_pista, wraplength=560)
        self.label_pista.pack()

        # --- Gráfica de evolución ---
        self.fig, self.ax = plt.subplots(figsize=(6, 3))
        self.ax.set_title("Distancia al número secreto por intento")
        self.ax.set_xlabel("Intento")
        self.ax.set_ylabel("Distancia")
        self.ax.grid(True)

        self.canvas = FigureCanvasTkAgg(self.fig, master=self.frame)
        self.canvas.get_tk_widget().pack(pady=10)

        # Botón Reintentar (inicialmente oculto)
        self.boton_reintentar = tk.Button(
            self.frame, text="Reintentar", font=self.fuente_normal,
            bg=self.color_boton_reintentar, fg="white", activebackground="#ef6c00",
            command=self.reintentar
        )
        self.boton_reintentar.pack(pady=10, fill="x")
        self.boton_reintentar.pack_forget()

    # --- Función para procesar los intentos ---
    def adivinar(self):
        try:
            intento = int(self.entrada.get())
        except ValueError:
            messagebox.showwarning("Entrada inválida", "Ingresa un número válido.")
            self.sonido_error.play()
            return

        if intento < self.rango_min or intento > self.rango_max:
            messagebox.showwarning("Número fuera de rango", f"Debe estar entre {self.rango_min} y {self.rango_max}.")
            self.sonido_error.play()
            return

        self.intentos.append(intento)
        self.entrada.delete(0, tk.END)

        # Lógica principal
        if intento == self.numero_secreto:
            self.puntaje = max(0, 100 - int(100 * (len(self.intentos) - 1) / self.intentos_maximos))
            self.label_resultado.config(
                text=f"🎉 ¡Felicidades! Adivinaste en {len(self.intentos)} intentos.\nPuntaje: {self.puntaje}",
                fg=self.color_exito
            )
            self.sonido_correcto.play()
            self.terminar_juego()
        elif len(self.intentos) >= self.intentos_maximos:
            self.label_resultado.config(
                text=f"❌ Juego terminado. Se agotaron los intentos.\nEl número era {self.numero_secreto}.",
                fg=self.color_error
            )
            self.label_pista.config(text="")
            self.sonido_incorrecto.play()
            self.terminar_juego()
        elif intento < self.numero_secreto:
            self.label_resultado.config(text="El número es mayor.", fg="black")
            self.sonido_incorrecto.play()
            self.dar_pista(intento)
        else:
            self.label_resultado.config(text="El número es menor.", fg="black")
            self.sonido_incorrecto.play()
            self.dar_pista(intento)

        self.actualizar_grafica()

    # --- Función para generar pistas inteligentes ---
    def dar_pista(self, intento):
        pistas = []

        if self.numero_secreto % 2 == 0:
            pistas.append("El número secreto es par.")
        else:
            pistas.append("El número secreto es impar.")

        for m in [3, 5, 7]:
            if self.numero_secreto % m == 0:
                pistas.append(f"Es múltiplo de {m}.")
                break

        suma_digitos = sum(int(d) for d in str(self.numero_secreto))
        pistas.append(f"La suma de sus dígitos es {suma_digitos}.")

        diferencia = abs(intento - self.numero_secreto)
        if diferencia > 20:
            pistas.append("Estás bastante lejos.")
        elif diferencia > 10:
            pistas.append("Te estás acercando.")
        else:
            pistas.append("¡Estás muy cerca!")

        pista = rnd.choice(pistas)
        self.label_pista.config(text=f"Pista: {pista}")

    # --- Función para actualizar la gráfica ---
    def actualizar_grafica(self):
        distancias = [abs(i - self.numero_secreto) for i in self.intentos]
        self.ax.clear()
        self.ax.plot(range(1, len(self.intentos) + 1), distancias, marker='o', linestyle='-', color='blue')
        self.ax.set_title("Distancia al número secreto por intento")
        self.ax.set_xlabel("Intento")
        self.ax.set_ylabel("Distancia")
        self.ax.set_xlim(1, max(self.intentos_maximos, len(self.intentos)))
        self.ax.set_ylim(0, self.rango_max - self.rango_min)
        self.ax.grid(True)
        self.canvas.draw()

    # --- Función para terminar el juego (deshabilita botones) ---
    def terminar_juego(self):
        self.entrada.config(state="disabled")
        self.boton_adivinar.config(state="disabled")
        self.boton_reintentar.pack(pady=10, fill="x")

    # --- Función para reiniciar el juego ---
    def reintentar(self):
        self.master.destroy()
        root_config = tk.Tk()
        from ventanas.ventana_configuracion import VentanaConfiguracion
        VentanaConfiguracion(root_config)
        root_config.mainloop()
