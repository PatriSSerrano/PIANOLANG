import pygame
import pygame.midi
import time
import threading
import sys

LETRA_A_NOTA = {
    'A': 48, 'Á': 48, 'B': 49, 'C': 50, 'D': 51, 
    'E': 52, 'É': 52, 'F': 53, 'G': 54, 'H': 55, 
    'I': 56, 'Í': 56, 'J': 57, 'K': 58, 'L': 59, 
    'M': 60, 'N': 61, 'Ñ': 62, 'O': 63, 'Ó': 63, 
    'P': 64, 'Q': 65, 'R': 66, 'S': 67, 'T': 68, 
    'U': 69, 'Ú': 69, 'Ü': 69, 'V': 70, 'W': 71, 
    'X': 72, 'Y': 73, 'Z': 74
}

NOTA_A_LETRA = {
    48: 'A', 49: 'B', 50: 'C', 51: 'D', 52: 'E', 53: 'F', 54: 'G',
    55: 'H', 56: 'I', 57: 'J', 58: 'K', 59: 'L', 60: 'M', 61: 'N',
    62: 'Ñ', 63: 'O', 64: 'P', 65: 'Q', 66: 'R', 67: 'S', 68: 'T',
    69: 'U', 70: 'V', 71: 'W', 72: 'X', 73: 'Y', 74: 'Z'
}

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

def hilo_terminal():
    print("🎹 COMPILADOR MELODYCODE (V2) INICIADO 🎹")
    print("La ventana del piano se ha abierto. Escribe aquí y pulsa Enter.")
    print("Escribe 'salir' para cerrar.\n")
    while True:
        texto = input(">> ")
        cola_comandos.append(texto)
        if texto.lower() == 'salir': break

def ejecutar_interprete():
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

if __name__ == "__main__":
    ejecutar_interprete()