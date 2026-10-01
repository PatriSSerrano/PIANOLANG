# CONEXIÓN: Importamos el archivo de la lógica
import modulos_melody

if __name__ == "__main__":
    print("="*40)
    print(" BIENVENIDO A MELODYCODE ".center(40, "="))
    print("="*40)
    print("1. Escuchar piano en vivo (Audio -> Texto)")
    print("2. Escribir código (Texto -> Audio)")
    
    opcion = input("\nElige (1 o 2): ")
    
    if opcion == '1': 
        modulos_melody.modo_audio_a_texto()
    elif opcion == '2': 
        modulos_melody.modo_texto_a_audio()
    else: 
        print("Opción no válida. Saliendo...")