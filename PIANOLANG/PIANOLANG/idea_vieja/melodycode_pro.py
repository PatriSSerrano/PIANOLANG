import pygame
import pygame.midi
import time
import threading
import sys
import math

try:
    import pyaudio
    import numpy as np
except ImportError:
    print("Faltan librerías. Ejecuta: pip install pyaudio numpy pygame")
    sys.exit()

# 1. MAPEO ERGONÓMICO (QWERTY DEL PIANO)
NOTA_A_LETRA = {
    48: 'M', 49: 'Q', 50: 'P', 51: 'H', 52: 'B', 53: 'F', 54: 'J', 55: 'G', 56: 'Z', 57: 'V', 58: 'X', 59: 'Y',
    60: 'E', 61: 'D', 62: 'A', 63: 'L', 64: 'O', 65: 'S', 66: 'C', 67: 'R', 68: 'T', 69: 'N', 70: 'U', 71: 'I',
    72: 'Ñ', 73: 'K', 74: 'W'
}

LETRA_A_NOTA = {v: k for k, v in NOTA_A_LETRA.items()}
LETRA_A_NOTA.update({'Á': 62, 'É': 60, 'Í': 71, 'Ó': 64, 'Ú': 70, 'Ü': 70})

NOTAS_BLANCAS = [48, 50, 52, 53, 55, 57, 59, 60, 62, 64, 65, 67, 69, 71, 72, 74]
NOTAS_NEGRAS = {49: 25, 51: 65, 54: 145, 56: 185, 58: 225, 61: 305, 63: 345, 66: 425, 68: 465, 70: 505, 73: 585}
BLANCO, NEGRO, COLOR_ACTIVO, GRIS = (255, 255, 255), (0, 0, 0), (0, 200, 100), (200, 200, 200)
FONDO_TEXTO, TEXTO_VERDE = (30, 30, 30), (0, 255, 100)

cola_comandos = []

def dibujar_piano(pantalla, fuente_teclas, fuente_terminal, nota_activa=None, texto_mostrado=""):
    pantalla.fill(GRIS)
    for i, nota in enumerate(NOTAS_BLANCAS):
        x = i * 40
        color = COLOR_ACTIVO if nota == nota_activa else BLANCO
        pygame.draw.rect(pantalla, color, (x, 0, 40, 200))
        pygame.draw.rect(pantalla, NEGRO, (x, 0, 40, 200), 2) 
        if nota in NOTA_A_LETRA:
            texto = fuente_teclas.render(NOTA_A_LETRA[nota], True, NEGRO)
            pantalla.blit(texto, (x + 13, 170))

    for nota, x in NOTAS_NEGRAS.items():
        color = COLOR_ACTIVO if nota == nota_activa else NEGRO
        pygame.draw.rect(pantalla, color, (x, 0, 30, 120))
        if nota in NOTA_A_LETRA:
            texto = fuente_teclas.render(NOTA_A_LETRA[nota], True, BLANCO)
            pantalla.blit(texto, (x + 8, 95))

    ancho = pantalla.get_width()
    pygame.draw.rect(pantalla, FONDO_TEXTO, (0, 200, ancho, 80))
    pygame.draw.line(pantalla, COLOR_ACTIVO, (0, 200), (ancho, 200), 3)

    if texto_mostrado:
        img_texto = fuente_terminal.render("> " + texto_mostrado, True, TEXTO_VERDE)
        pantalla.blit(img_texto, (20, 225))
    pygame.display.flip()

# ==========================================
# MODO 1: AUDIO -> TEXTO (MICRÓFONO)
# ==========================================
def modo_audio_a_texto():
    pygame.init()
    pantalla = pygame.display.set_mode((len(NOTAS_BLANCAS) * 40, 280))
    pygame.display.set_caption("MelodyCode - Escuchando Piano...")
    fuente_teclas = pygame.font.SysFont("Arial", 16, bold=True)
    fuente_terminal = pygame.font.SysFont("Consolas", 24, bold=True)

    p = pyaudio.PyAudio()
    buffer_size = 2048 
    try:
        stream = p.open(format=pyaudio.paFloat32, channels=1, rate=44100, input=True, frames_per_buffer=buffer_size)
    except Exception as e:
        print("Error abriendo micrófono:", e)
        sys.exit()

    print("\n🎤 Micro activado. Toca una tecla en tu piano (o acércate a una app de piano de móvil)...")
    texto_acumulado, nota_actual, corriendo = "", None, True
    ultima_vez_sonido = time.time()

    dibujar_piano(pantalla, fuente_teclas, fuente_terminal, texto_mostrado=texto_acumulado)

    while corriendo:
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT: corriendo = False

        try:
            data = stream.read(buffer_size, exception_on_overflow=False)
            muestras = np.frombuffer(data, dtype=np.float32)
            volumen = np.sum(muestras**2) / len(muestras)
        except:
            volumen = 0

        if volumen > 0.005:
            muestras_padded = np.pad(muestras, (0, 8192 - len(muestras)))
            fft_data = np.fft.rfft(muestras_padded)
            magnitudes = np.abs(fft_data)
            freqs = np.fft.rfftfreq(len(muestras_padded), 1.0/44100)
            
            tono = freqs[np.argmax(magnitudes)]
            
            if 100 < tono < 4000: 
                nota_midi = int(round(12 * math.log2(tono / 440.0) + 69))
                if nota_midi in NOTA_A_LETRA and nota_midi != nota_actual:
                    nota_actual = nota_midi
                    letra = NOTA_A_LETRA[nota_midi]
                    texto_acumulado += letra
                    print(f"Frecuencia: {tono:.1f}Hz -> Nota MIDI {nota_midi} -> Letra {letra}")
                    dibujar_piano(pantalla, fuente_teclas, fuente_terminal, nota_activa=nota_midi, texto_mostrado=texto_acumulado)
                    ultima_vez_sonido = time.time()
        else:
            if time.time() - ultima_vez_sonido > 0.5 and nota_actual is not None:
                nota_actual = None
                dibujar_piano(pantalla, fuente_teclas, fuente_terminal, texto_mostrado=texto_acumulado)
            
            if time.time() - ultima_vez_sonido > 2.0 and len(texto_acumulado) > 0 and texto_acumulado[-1] != " ":
                texto_acumulado += " "
                dibujar_piano(pantalla, fuente_teclas, fuente_terminal, texto_mostrado=texto_acumulado)

    stream.stop_stream()
    stream.close()
    p.terminate()
    pygame.quit()

# ==========================================
# MODO 2: TEXTO -> AUDIO (CÓDIGO A MÚSICA)
# ==========================================
def hilo_terminal():
    while True:
        texto = input(">> ")
        cola_comandos.append(texto)
        if texto.lower() == 'salir': break

def modo_texto_a_audio():
    pygame.init()
    pygame.midi.init()
    pantalla = pygame.display.set_mode((len(NOTAS_BLANCAS) * 40, 280))
    pygame.display.set_caption("MelodyCode - Ejecución en vivo")
    fuente_teclas = pygame.font.SysFont("Arial", 16, bold=True)
    fuente_terminal = pygame.font.SysFont("Consolas", 24, bold=True) 
    
    puerto = pygame.midi.get_default_output_id()
    if puerto == -1: sys.exit("Error MIDI. No hay sintetizador.")
    reproductor = pygame.midi.Output(puerto)
    reproductor.set_instrument(0)

    print("\n🎹 COMPILADOR MELODYCODE INICIADO 🎹")
    print("La ventana del piano se ha abierto. Escribe aquí y pulsa Enter.")
    
    threading.Thread(target=hilo_terminal, daemon=True).start()
    corriendo, texto_acumulado = True, ""
    dibujar_piano(pantalla, fuente_teclas, fuente_terminal)

    while corriendo:
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT: corriendo = False

        if cola_comandos:
            frase = cola_comandos.pop(0)
            if frase.lower() == 'salir': break
            if frase.strip() != "":
                texto_acumulado = ""
                for caracter in frase:
                    pygame.event.pump() 
                    texto_acumulado += caracter 
                    if caracter == ' ':
                        dibujar_piano(pantalla, fuente_teclas, fuente_terminal, texto_mostrado=texto_acumulado)
                        time.sleep(0.4)
                        continue
                        
                    letra_base = caracter.upper()
                    if letra_base in LETRA_A_NOTA:
                        nota = LETRA_A_NOTA[letra_base]
                        duracion = 0.6 if caracter.isupper() else 0.25
                        dibujar_piano(pantalla, fuente_teclas, fuente_terminal, nota_activa=nota, texto_mostrado=texto_acumulado)
                        reproductor.note_on(nota, 127)
                        time.sleep(duracion)
                        reproductor.note_off(nota, 127)
                        dibujar_piano(pantalla, fuente_teclas, fuente_terminal, texto_mostrado=texto_acumulado)
        time.sleep(0.05)
    del reproductor
    pygame.midi.quit()
    pygame.quit()

# ==========================================
# MENÚ PRINCIPAL
# ==========================================
if __name__ == "__main__":
    print("="*40)
    print(" BIENVENIDO A MELODYCODE ".center(40, "="))
    print("="*40)
    print("1. Escuchar piano en vivo (Audio -> Texto)")
    print("2. Escribir código (Texto -> Audio)")
    
    opcion = input("\nElige (1 o 2): ")
    if opcion == '1': modo_audio_a_texto()
    elif opcion == '2': modo_texto_a_audio()
    else: print("Opción no válida. Saliendo...")