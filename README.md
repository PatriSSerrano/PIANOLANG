# MelodyCode (Piano-Lang)

**Un Lenguaje de Programación Esotérico basado en Interpretación Musical.**

MelodyCode nace con la misión de democratizar la programación a través de la expresión artística. En este lenguaje, el código fuente es texto y el código máquina es música. Programar ya no es picar texto en una consola fría, sino interpretar una pieza al piano donde la armonía, el ritmo y el tiempo generan la lógica del software.

Este proyecto ha sido desarrollado como práctica de Lenguajes de Programación Esotéricos.

---

## Evolución del Proyecto

El desarrollo de MelodyCode se ha dividido en dos grandes fases de ingeniería, cada una con un enfoque distinto sobre la interacción persona-ordenador:

### Fase 1: El Prototipo Inicial (Basado en Tiempo)
* **Archivo:** `piano_lang.py` (Versión antigua)
* **Concepto:** El teclado del ordenador emula un piano. Cada tecla representa una nota y una letra del abecedario.
* **Gramática:** Basada en la duración de la pulsación.
  * **Minúsculas (Comandos):** Pulsaciones cortas (staccato, < 1.5s).
  * **Mayúsculas (Variables):** Pulsaciones largas (sostenidas, > 1.5s).
  * **Ejecución:** Los silencios superiores a 2.5 segundos actúan como el delimitador final para compilar y ejecutar la instrucción.

### Fase 2: Versión Final Modular (Bidireccional y Señales Reales)
* **Archivo principal:** `main.py`
* **Concepto:** Arquitectura modular orientada a la eficiencia y al procesamiento de señales de audio reales. Permite dos modos de ejecución:
  1. **Texto ➔ Audio (Compilador Musical):** El usuario escribe código en la terminal y el programa lo traduce en tiempo real a eventos MIDI, reproduciendo la melodía y visualizando las teclas pulsadas en una interfaz gráfica con *scroll automático*.
  2. **Audio ➔ Texto (Intérprete Acústico):** El sistema abre el micrófono y escucha a un piano real. Utiliza matemáticas puras (**Transformada Rápida de Fourier - FFT** mediante `numpy`) para analizar las ondas de sonido, detectar la frecuencia (Hz) en tiempo real, filtrar el ruido ambiente y traducir las notas tocadas a código en pantalla.

---

## Diseño de la Sintaxis: El "QWERTY" del Piano

En lugar de un simple mapeo alfabético (A=Do, B=Re...), MelodyCode implementa un **diseño ergonómico basado en la frecuencia de uso de las letras en el idioma español**, minimizando el desplazamiento de las manos sobre el instrumento:

| Zona del Piano | Nivel de Accesibilidad | Letras Asignadas |
| :--- | :--- | :--- |
| **Blancas Centrales** (Octava 4) | **Máximo** (Posición natural de las manos) | Las más usadas: **E, A, O, S, R, N, C...** |
| **Negras Centrales** (Octava 4) | **Alto** (Fáciles de alcanzar) | Consonantes comunes: **D, L, T, I, U** |
| **Exteriores** (Octavas 3 y 5) | **Medio / Bajo** (Requieren desplazamiento) | Letras menos frecuentes: **Z, X, W, K, Ñ, Q** |

*Nota sobre las tildes: Las vocales acentuadas (Á, É, Í...) se mapean a la misma frecuencia que su vocal base para mantener la coherencia armónica de las palabras sin alterar la melodía por reglas ortográficas.*

---

## Instalación y Requisitos

Para ejecutar el intérprete en tu máquina local, necesitas tener instalado **Python 3.x**. 

1. Clona este repositorio:
   ```bash
   git clone [https://github.com/TU_USUARIO/TU_REPOSITORIO.git](https://github.com/TU_USUARIO/TU_REPOSITORIO.git)
   cd TU_REPOSITORIO
