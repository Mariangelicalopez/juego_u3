# Importamos el módulo tkinter para crear interfaces gráficas
import tkinter as tk

# Importamos nuestra clase VentanaConfiguracion desde la carpeta 'ventanas'
from ventanas.ventana_configuracion import VentanaConfiguracion

# Definimos la función principal del programa
def main():
    # Creamos una nueva ventana de Tkinter que servirá como la ventana principal de configuración
    root_config = tk.Tk()
    
    # Creamos una instancia de VentanaConfiguracion y le pasamos la ventana principal (root_config)
    app = VentanaConfiguracion(root_config)
    
    # Iniciamos el bucle principal de eventos de Tkinter
    root_config.mainloop()

if __name__ == "__main__":
    main()

