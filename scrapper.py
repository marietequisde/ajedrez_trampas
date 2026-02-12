from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager
import time
import sunfish

url_ajedrez = "https://www.chesskid.com/es/play/computer"

def iniciar_navegador(url):
    options = webdriver.ChromeOptions()
    options.add_experimental_option("detach", True)
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)
    driver.get(url)
    return driver

def scrape_chess_board(driver):
    # IMPORTANTE: Usamos ".." para celdas vacías para que la función FEN sea precisa
    board = [[".." for _ in range(8)] for _ in range(8)]
    try:
        pieces = driver.find_elements(By.CSS_SELECTOR, ".piece")
        for piece in pieces:
            classes = piece.get_attribute("class")
            parts = classes.split(' ')
            
            # Extraer tipo (ej: 'wp') y posición (ej: 'square-81')
            p_type = [p for p in parts if len(p) == 2 and not p.isdigit()][0]
            pos_class = [p for p in parts if 'square-' in p][0]
            
            pos_num = int(pos_class.replace('square-', ''))
            col = (pos_num // 10) - 1
            row = 8 - (pos_num % 10)
            
            if 0 <= col < 8 and 0 <= row < 8:
                board[row][col] = p_type
        return board
    except Exception as e:
        print(f"Error leyendo piezas: {e}")
        return board

def matriz_a_fen(matriz, turno="w"):
    fen_rows = []
    mapeo = {'p': 'p', 'n': 'n', 'b': 'b', 'r': 'r', 'q': 'q', 'k': 'k'}
    
    for row in matriz:
        empty = 0
        fen_row = ""
        for cell in row:
            if cell == ".." or cell == " ":
                empty += 1
            else:
                if empty > 0:
                    fen_row += str(empty)
                    empty = 0
                color = cell[0]
                tipo = cell[1]
                letra = mapeo[tipo].upper() if color == 'w' else mapeo[tipo].lower()
                fen_row += letra
        if empty > 0:
            fen_row += str(empty)
        fen_rows.append(fen_row)
    
    return "/".join(fen_rows) + f" {turno} KQkq - 0 1"

def pensar_jugada_sunfish(matriz, es_blancas=True):
    turno = "w" if es_blancas else "b"
    posicion_fen = matriz_a_fen(matriz, turno)
    
    searcher = sunfish.Searcher()
    pos = sunfish.parseFEN(posicion_fen)
    
    # Buscamos durante 2 segundos
    move, score = searcher.search(pos, secs=2)
    return sunfish.render(move)

if __name__ == "__main__":
    print("¡Bienvenido al asistente de ajedrez con Sunfish!")
    main()