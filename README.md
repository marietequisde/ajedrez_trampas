# Chess Scraper & Analyzer (Asistente de Ajedrez)

Una aplicación de escritorio construida en Python que automatiza la lectura de un tablero de ajedrez en el navegador, procesa su estado y calcula la mejor jugada posible en tiempo real utilizando un motor de ajedrez integrado. 

El proyecto demuestra habilidades en automatización web, parseo del DOM, transformación de datos complejos a estándares universales (FEN) y desarrollo de interfaces gráficas de usuario (GUI).

## Características Principales

*   **Lectura del DOM en tiempo real:** Utiliza Selenium para abrir una sesión de Chrome, buscar el tablero HTML y extraer las coordenadas de cada pieza leyendo sus clases CSS (ej. `wp` para peón blanco, `square-81` para la posición).
*   **Conversión a formato FEN:** Un algoritmo lee la matriz 8x8 generada por el scraper y la transforma en una cadena FEN válida, calculando dinámicamente los espacios vacíos.
*   **Motor de Ajedrez Integrado:** Conecta la posición FEN con el motor **Sunfish** (un motor de ajedrez minimalista en Python) para calcular el movimiento óptimo.
*   **GUI Moderna y Asíncrona:** Interfaz construida con **CustomTkinter**. Utiliza `threading` para evitar bloqueos visuales durante la carga del navegador o el cálculo del motor. Además, procesa capturas del tablero usando `PIL` para reflejarlas en el panel de control.

## Tecnologías Utilizadas

*   **Lenguaje:** Python 3
*   **GUI:** CustomTkinter
*   **Web Scraping:** Selenium WebDriver, webdriver-manager
*   **Procesamiento de Imágenes:** Pillow (PIL), io
*   **Motor de Ajedrez:** Sunfish Engine
*   **Multithreading:** Módulo `threading` nativo.

## Instalación y Uso

Sigue estos pasos para probar el proyecto en tu entorno local:

1. Clona este repositorio:
```bash
   git clone [https://github.com/marietequisde/ajedrez_trampas.git](https://github.com/marietequisde/ajedrez_trampas.git)
   cd ajedrez_trampas
