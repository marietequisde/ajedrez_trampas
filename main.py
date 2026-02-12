import customtkinter as ctk
import threading
from PIL import Image
import io
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager

# Importamos tus archivos
import sunfish
from scrapper import scrape_chess_board, matriz_a_fen

class ChessScraperApp(ctk.CTk):
    def __init__(self):
        super().__init__()

        self.title("Chess Scraper")
        self.geometry("1100x700")
        self.driver = None

        # --- DISEÑO ---
        # Panel Izquierdo: Consola y Resultado
        self.left_panel = ctk.CTkFrame(self, width=400)
        self.left_panel.pack(side="left", fill="both", padx=10, pady=10)

        self.label_titulo = ctk.CTkLabel(self.left_panel, text="CONTROL PANEL", font=("Roboto", 20, "bold"))
        self.label_titulo.pack(pady=20)

        self.console = ctk.CTkTextbox(self.left_panel, height=200, font=("Consolas", 12))
        self.console.pack(fill="x", padx=10, pady=10)

        self.label_move = ctk.CTkLabel(self.left_panel, text="-- --", font=("Roboto", 60, "bold"), text_color="#f1c40f")
        self.label_move.pack(pady=30)

        self.btn_start = ctk.CTkButton(self.left_panel, text="1. ABRIR NAVEGADOR", command=self.start_browser)
        self.btn_start.pack(pady=5)

        self.btn_read = ctk.CTkButton(self.left_panel, text="2. LEER Y ANALIZAR", command=self.analizar_ahora, fg_color="#27ae60", height=50)
        self.btn_read.pack(pady=10)

        # Panel Derecho: Visor del Tablero (El "Espejo")
        self.right_panel = ctk.CTkFrame(self)
        self.right_panel.pack(side="right", fill="both", expand=True, padx=10, pady=10)
        
        self.board_display = ctk.CTkLabel(self.right_panel, text="El tablero aparecerá aquí\nal darle a 'LEER'", font=("Roboto", 16))
        self.board_display.pack(fill="both", expand=True)

    def log(self, text):
        self.console.insert("end", f"\n> {text}")
        self.console.see("end")

    def start_browser(self):
        threading.Thread(target=self.init_driver, daemon=True).start()

    def init_driver(self):
        self.log("Iniciando Chrome...")
        options = webdriver.ChromeOptions()
        options.add_experimental_option("detach", True)
        self.driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)
        self.driver.get("https://www.chesskid.com/es/play/computer")
        self.log("Navegador listo.")

    def analizar_ahora(self):
        if not self.driver:
            self.log("¡Error! Abre el navegador primero.")
            return

        try:
            # 1. CAPTURA VISUAL (Solo en este momento)
            # Buscamos el elemento del tablero en el HTML
            board_elem = self.driver.find_element(By.CSS_SELECTOR, "chess-board, .board, #board")
            screenshot = board_elem.screenshot_as_png
            img = Image.open(io.BytesIO(screenshot))
            
            # Ajustamos la imagen al tamaño del panel derecho
            img_ctk = ctk.CTkImage(light_image=img, dark_image=img, size=(550, 550))
            self.board_display.configure(image=img_ctk, text="")

            # 2. SCRAPING DE DATOS
            self.log("Leyendo piezas...")
            tablero = scrape_chess_board(self.driver)
            fen = matriz_a_fen(tablero, turno="w")

            # 3. CÁLCULO CON MOTOR
            self.log("Calculando mejor jugada...")
            searcher = sunfish.Searcher()
            pos = sunfish.parseFEN(fen)
            
            # Buscamos el mejor movimiento (2 segundos de análisis)
            move, _ = searcher.search(pos, secs=2)
            movimiento_str = sunfish.render(move)

            # 4. MOSTRAR RESULTADO
            self.label_move.configure(text=movimiento_str.upper())
            self.log(f"Resultado: {movimiento_str}")

        except Exception as e:
            self.log(f"Error: {str(e)}")

if __name__ == "__main__":
    app = ChessScraperApp()
    app.mainloop()