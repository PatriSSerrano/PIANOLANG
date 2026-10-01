import pygame
import pygame.midi
import time
import threading
import sys
import math
import pyaudio
import numpy as np

# CONEXIÓN: Importamos todo lo del archivo teclado_ui.py
from teclado_ui import *

cola_comandos = []

def modo_audio_a_texto():
    pygame.init()
    pantalla = pygame.display.set_mode((len(NOTAS_BLANCAS) * 40, 280))
    pygame.display.set_caption("MelodyCode - Escuchando Piano...")
    fuente_teclas = pygame.font.SysFont("Arial", 16, bold=True)
    fuente_terminal = pygame.font.SysFont("Consolas", 24, bold=True)

    p = pyaudio.PyAudio()
    try:
        stream = p.open(format=pyaudio.paFloat32, channels=1, rate=44100, input=True, frames_per_buffer=2048)
    except Exception as e:
        print("Error abriendo micrófono:", e)
        sys.exit()

    print("\n🎤 Micro activado. Toca una tecla en tu piano...")
    texto_acumulado, nota_actual, corriendo = "", None, True
    ultima_vez_sonido = time.time()

    dibujar_piano(pantalla, fuente_teclas, fuente_terminal, texto_mostrado=texto_acumulado)

    while corriendo:
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT: corriendo = False

        try:
            data = stream.read(2048, exception_on_overflow=False)
            muestras = np.frombuffer(data, dtype=np.float32)
            volumen = np.sum(muestras**2) / len(muestras)
        except:
            volumen = 0

        if volumen > 0.005:
            muestras_padded = np.pad(muestras, (0, 8192 - len(muestras)))
            fft_data = np.fft.rfft(muestras_padded)
            tono = np.fft.rfftfreq(len(muestras_padded), 1.0/44100)[np.argmax(np.abs(fft_data))]
            
            if 100 < tono < 4000: 
                nota_midi = int(round(12 * math.log2(tono / 440.0) + 69))
                if nota_midi in NOTA_A_LETRA and nota_midi != nota_actual:
                    nota_actual = nota_midi
                    texto_acumulado += NOTA_A_LETRA[nota_midi]
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

    print("\n🎹 COMPILADOR INICIADO. Escribe aquí y pulsa Enter.")
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
                        
                    letra = caracter.upper()
                    if letra in LETRA_A_NOTA:
                        nota = LETRA_A_NOTA[letra]
                        dibujar_piano(pantalla, fuente_teclas, fuente_terminal, nota_activa=nota, texto_mostrado=texto_acumulado)
                        reproductor.note_on(nota, 127)
                        time.sleep(0.6 if caracter.isupper() else 0.25)
                        reproductor.note_off(nota, 127)
                        dibujar_piano(pantalla, fuente_teclas, fuente_terminal, texto_mostrado=texto_acumulado)
        time.sleep(0.05)
    del reproductor
    pygame.midi.quit()
    pygame.quit()