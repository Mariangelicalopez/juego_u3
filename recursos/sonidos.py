# recursos/sonidos.py
import numpy as np   # Para cálculos matemáticos y generación de ondas senoidales
import io           # Para manejar flujos de bytes en memoria
import wave         # Para crear archivos WAV
import struct       # Para empaquetar datos binarios

def generar_sonido_tono(freq, duration):
    """
    Genera un sonido WAV en memoria con una frecuencia y duración dadas.

    Parámetros:
    freq (float): frecuencia del tono en Hz
    duration (float): duración del sonido en segundos

    Retorna:
    BytesIO: objeto en memoria que contiene el archivo WAV generado,
             que puede usarse directamente con pygame.mixer.Sound.
    """
    framerate = 44100       # Frecuencia de muestreo estándar (samples por segundo)
    amplitude = 32767       # Amplitud máxima para onda de 16 bits (valor máximo)
    n_samples = int(framerate * duration)  # Número total de muestras para la duración dada

    buf = io.BytesIO()      # Buffer en memoria para guardar el archivo WAV

    # Abrimos un archivo WAV en modo escritura dentro del buffer en memoria
    with wave.open(buf, 'wb') as wav_file:
        wav_file.setnchannels(1)          # Mono (1 canal)
        wav_file.setsampwidth(2)          # 2 bytes por muestra (16 bits)
        wav_file.setframerate(framerate) # Frecuencia de muestreo

        # Generamos cada muestra de la onda senoidal
        for i in range(n_samples):
            # Calculamos el valor de la muestra en formato entero
            value = int(amplitude * np.sin(2 * np.pi * freq * i / framerate))
            # Empaquetamos el valor en formato binario de 2 bytes (little-endian)
            data = struct.pack('<h', value)
            # Escribimos la muestra en el archivo WAV
            wav_file.writeframesraw(data)

    buf.seek(0)  # Volvemos al inicio del buffer para que pueda ser leído desde el principio
    return buf   # Retornamos el buffer con el archivo WAV generado
