import pygame
import time
import sys

pygame.init()
screen = pygame.display.set_mode((400, 200))
pygame.display.set_caption("Interprete de MelodyCode / Piano-Lang")

KEY_MAPPING = {
    pygame.K_z: 'A', pygame.K_s: 'B', pygame.K_x: 'C', pygame.K_d: 'D', 
    pygame.K_c: 'E', pygame.K_v: 'F', pygame.K_g: 'G', pygame.K_b: 'H', 
    pygame.K_h: 'I', pygame.K_n: 'J', pygame.K_j: 'K', pygame.K_m: 'L',
    pygame.K_q: 'M', pygame.K_2: 'N', pygame.K_w: 'Ñ', pygame.K_3: 'O', 
    pygame.K_e: 'P', pygame.K_r: 'Q', pygame.K_5: 'R', pygame.K_t: 'S', 
    pygame.K_6: 'T', pygame.K_y: 'U', pygame.K_7: 'V', pygame.K_u: 'W', 
    pygame.K_i: 'X', pygame.K_9: 'Y', pygame.K_o: 'Z',
}

key_press_start = {} 
last_key_release_time = time.time()
current_word = ""

print("🎹 Intérprete MelodyCode Iniciado (V1).")
print("Toca usando el teclado del PC (Z-M para graves, Q-O para agudas).")
print("Pulsa ESC o cierra la ventana para salir.\n")
print("-" * 50)

running = True
while running:
    current_time = time.time()

    if current_word and (current_time - last_key_release_time > 2.5):
        print(f"\n>> [EJECUTANDO COMANDO]: {current_word}\n")
        print("-" * 50)
        current_word = "" 

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                running = False
            elif event.key in KEY_MAPPING:
                key_press_start[event.key] = current_time
        elif event.type == pygame.KEYUP:
            if event.key in KEY_MAPPING and event.key in key_press_start:
                duration = current_time - key_press_start[event.key]
                letter = KEY_MAPPING[event.key]
                if duration < 1.5:
                    char = letter.lower()
                    tipo = "Corto"
                else:
                    char = letter.upper()
                    tipo = "Largo"

                current_word += char
                print(f"♫ Nota ({letter}) | Duración: {duration:.2f}s [{tipo}] ➔ Registrado: {char} | Buffer: {current_word}")
                last_key_release_time = current_time
                del key_press_start[event.key]

pygame.quit()
sys.exit()