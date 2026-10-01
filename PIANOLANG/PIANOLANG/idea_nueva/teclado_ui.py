import pygame

# MAPEO ERGONÓMICO
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
        frase_completa = "> " + texto_mostrado
        img_texto = fuente_terminal.render(frase_completa, True, TEXTO_VERDE)
        
        # LÓGICA DEL SCROLL:
        ancho_texto = img_texto.get_width()
        max_ancho_permitido = ancho - 40 # 40 píxeles de margen
        
        # Si el texto es más largo que la pantalla, calculamos cuánto se sale
        # y lo desplazamos hacia la izquierda usando una coordenada X negativa.
        if ancho_texto > max_ancho_permitido:
            posicion_x = 20 - (ancho_texto - max_ancho_permitido)
        else:
            posicion_x = 20
            
        pantalla.blit(img_texto, (posicion_x, 225))
        
    pygame.display.flip()