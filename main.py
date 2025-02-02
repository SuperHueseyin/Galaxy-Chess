import sys
import pygame as p
from Game import Game
from Board import Board
from stockfish import Stockfish

# Global Variable
#stockfish = Stockfish(path="stockfish/linux/stockfish-ubuntu-x86-64", parameters={"Threads": 2, "Skill Level": 10}) # Ubuntu User
#stockfish = Stockfish(path="stockfish/win/stockfish-windows-x86-64-sse41-popcnt.exe", parameters={"Threads": 2, "Skill Level": 10}) # Windows User
game = Game()
board = Board(game.screen)

# Übersetzt die Abkürzungen der Figuren in Namen
def get_piece_name(figur):
    namen = {
        "bR": "Schwarzer Turm",
        "bN": "Schwarzer Springer",
        "bB": "Schwarzer Läufer",
        "bQ": "Schwarze Dame",
        "bK": "Schwarzer König",
        "bP": "Schwarzer Bauer",
        "wR": "Weißer Turm",
        "wN": "Weißer Springer",
        "wB": "Weißer Läufer",
        "wQ": "Weiße Dame",
        "wK": "Weißer König",
        "wP": "Weißer Bauer"
    }
    return namen.get(figur)

# Ein Schachbrett zeichnen
def render_chess_game(screen, board, feld_size, selected_square, possible_moves=None, king_death_position=None):
    color_light = (240, 217, 181)  # Hellbraun
    color_dark = (181, 136, 99)  # Dunkelbraun
    color_selection = (255, 215, 0)  # Gold für Auswahl
    color_possible_selection = (135, 206, 250)  # Blau für mögliche Züge
    color_red = (255, 0, 0)  # Rot für das Feld unter dem König

    piece_images = {
        "bR": p.image.load("img/bR.png"),
        "bN": p.image.load("img/bN.png"),
        "bB": p.image.load("img/bB.png"),
        "bQ": p.image.load("img/bQ.png"),
        "bK": p.image.load("img/bK.png"),
        "bP": p.image.load("img/bP.png"),
        "wR": p.image.load("img/wR.png"),
        "wN": p.image.load("img/wN.png"),
        "wB": p.image.load("img/wB.png"),
        "wQ": p.image.load("img/wQ.png"),
        "wK": p.image.load("img/wK.png"),
        "wP": p.image.load("img/wP.png")
    }

    for key in piece_images:
        piece_images[key] = p.transform.scale(piece_images[key], (feld_size, feld_size))

    # Schachbrett zeichnen
    for row in range(8):
        for column in range(8):
            if (row + column) % 2 == 0:
                color = color_light
            else:
                color = color_dark

            if selected_square == (row, column):
                color = color_selection

            # Wenn das Feld unter dem König geschlagen wurde, färbe es rot
            if king_death_position and king_death_position == (row, column):
                color = color_red

            if possible_moves and (row, column) in possible_moves:
                color = color_possible_selection

            p.draw.rect(screen, color, p.Rect(column * feld_size, row * feld_size, feld_size, feld_size))

            figur = board[row][column]
            if figur:
                screen.blit(piece_images[figur], (column * feld_size, row * feld_size))

# Textfeld für Züge zeichnen
def render_move_history(screen, moves_list):
    text_rect = p.Rect(660, 10, 400, 620)  # Bereich des Textfelds
    p.draw.rect(screen, (181, 126, 79), text_rect)  # Hintergrundfarbe

    # Maximal 20 Züge anzeigen (nur die letzten)
    max_display_moves = 20
    last_moves = moves_list[-max_display_moves:]  # Nur die letzten X Züge holen

    # Züge anzeigen
    font = p.font.SysFont("Arial", 25)
    y_offset = 20  # Abstand zum oberen Rand des Textfelds
    for i, zug in enumerate(last_moves, start=max(1, len(moves_list) - max_display_moves + 1)):
        game.set_text(f"{i}. {zug}", 20, (0, 0, 0), False, (670, y_offset) )
        y_offset += 25  # Abstand zwischen den Einträgen

# Auswahlmenü für Umwandlung
def bauernumwandlung(screen, player_color):
    screen.fill((220, 197, 161))  # Hintergrundfarbe

    font = p.font.SysFont("Arial", 36, True)
    game.set_text("Wähle die neue Figur:", 36, (0, 0, 0), False, (360, 100))

    if player_color == "w":  # Weißer Spieler
        piece_types = ["Dame", "Turm", "Springer", "Läufer"]
        piece_images = {
            "Dame": p.image.load("img/wQ.png"),  # Weiße Dame Bild
            "Turm": p.image.load("img/wR.png"),  # Weißer Turm Bild
            "Springer": p.image.load("img/wN.png"),  # Weißer Springer Bild
            "Läufer": p.image.load("img/wB.png")   # Weißer Läufer Bild
        }
    else:  # Schwarzer Spieler
        piece_types = ["Dame", "Turm", "Springer", "Läufer"]
        piece_images = {
            "Dame": p.image.load("img/bQ.png"),  # Schwarze Dame Bild
            "Turm": p.image.load("img/bR.png"),  # Schwarzer Turm Bild
            "Springer": p.image.load("img/bN.png"),  # Schwarzer Springer Bild
            "Läufer": p.image.load("img/bB.png")   # Schwarzer Läufer Bild
        }
    
    # Bildgröße anpassen (für die Darstellung im Menü)
    bild_size = (60, 60)
    for key in piece_images:
        piece_images[key] = p.transform.scale(piece_images[key], bild_size)

    buttons = []
    for i, figur in enumerate(piece_types):
        button = p.Rect(370, 200 + i * 100, 200, 60)
        buttons.append((button, figur))
        
        # Rechteck für den Button zeichnen
        p.draw.rect(screen, (0, 0, 0), button)
        
        # Text anzeigen
        text_color = (255, 255, 255)
        game.set_text(figur, 30, text_color, False, button.x + 50, button.y + 15)
        
        # Bild anzeigen
        screen.blit(piece_images[figur], (button.x + 200, button.y + 0))

    p.display.flip()

    while True:
        for event in p.event.get():
            if event.type == p.QUIT:
                p.quit()
                sys.exit()
            if event.type == p.MOUSEBUTTONDOWN:
                maus_x, maus_y = p.mouse.get_pos()
                for button, figur in buttons:
                    if button.collidepoint(maus_x, maus_y):
                        return figur

# Überprüft, ob der gegnerische/eigner Spieler König geschlagen wurde #todo: Hier wird nur auf gegner geprüft, hier auf spieler PRÜFEN ob  König von der KI geschlagen wird
def win_state(board_state, current_player):
    next_player = "b" if current_player == "w" else "w"
    for row in range(8):
        for column in range(8):
            if board_state[row][column] == f"{next_player}K":
                return False  # Der gegnerische König ist noch auf dem Brett

    return True  # Der gegnerische König wurde geschlagen

def convert_board_to_fen(board_state, active_player, rochade_rechte, en_passant_feld, move_counter):
    """
    Konvertiert das Schachbrett in das FEN-Format.
    :param board_state: 2D-Liste mit Figuren (z. B. "wP", "bK", "", etc.)
    :param active_player: "w" oder "b", je nachdem, welcher Spieler am Zug ist
    :param rochade_rechte: String, z. B. "KQkq", gibt Rochade-Möglichkeiten an
    :param en_passant_feld: En-Passant-Feld, z. B. "e3", oder "-" falls nicht möglich
    :param move_counter: Aktuelle Zugnummer
    :return: String im FEN-Format
    """
    fen = ""

    # 1. Spielfeld in FEN umwandeln
    for row in board_state:
        empty_square_count = 0
        for field in row:
            if field == "":
                empty_square_count += 1
            else:
                if empty_square_count > 0:
                    fen += str(empty_square_count)
                    empty_square_count = 0
                fen += field[1].upper() if field[0] == "w" else field[1].lower()
        if empty_square_count > 0:
            fen += str(empty_square_count)
        fen += "/"
    fen = fen[:-1]  # Entferne den letzten Slash

    # 2. Spieler am Zug
    fen += f" {active_player} "

    # 3. Rochaderechte
    fen += rochade_rechte if rochade_rechte else "-"

    # 4. En-Passant-Feld
    fen += f" {en_passant_feld} "

    # 5. Halbzüge (für 50-Züge-Regel, aktuell auf 0 gesetzt, falls nicht gespeichert)
    fen += "0 "

    # 6. Zugnummer
    fen += str(move_counter)

    return fen

def calculate_castling_rights(board_state, piece_movements):
    rochade_rechte = ""

    # Prüfen, ob sich der weiße König oder Türme bewegt haben
    if "wK" in board_state[7][4]:
        if "wR" in board_state[7][7] and "Ke1 nach h1" not in piece_movements:
            rochade_rechte += "K"
        if "wR" in board_state[7][0] and "Ke1 nach a1" not in piece_movements:
            rochade_rechte += "Q"

    # Prüfen, ob sich der schwarze König oder Türme bewegt haben
    if "bK" in board_state[0][4]:
        if "bR" in board_state[0][7] and "Ke8 nach h8" not in piece_movements:
            rochade_rechte += "k"
        if "bR" in board_state[0][0] and "Ke8 nach a8" not in piece_movements:
            rochade_rechte += "q"

    return rochade_rechte if rochade_rechte else "-"

def calculate_en_passant_square(move_list):
    if not move_list:
        return "-"

    latest_move = move_list[-1]  # Letzten Zug holen, z. B. "Bauer von E2 nach E4"
    move_details = latest_move.split()   # Zerlegen: ["Bauer", "von", "E2", "nach", "E4"]

    if "Bauer" in move_details and "von" in move_details and "nach" in move_details:
        start_pos = move_details[2]  # E2
        target_position = move_details[4]   # E4

        if len(start_pos) == 2 and len(target_position) == 2:
            start_column, start_row = start_pos[0], int(start_pos[1])
            target_column, target_row = target_position[0], int(target_position[1])

            if abs(start_row - target_row) == 2:  # Bauer ist 2 Felder gezogen
                en_passant_feld = start_column + str((start_row + target_row) // 2)
                return en_passant_feld.lower()  # FEN benötigt Kleinbuchstaben für Spalten

    return "-"

def is_valid_chess_move(board_state, start_position, target_position, player_color):
    """
    Prüft, ob der Zug von `start` nach `ziel` für die aktuelle `spieler_farbe` erlaubt ist.
    """
    row_1, column_1 = start_position
    row_2, column_2 = target_position
    figur = board_state[row_1][column_1]

    if not figur or figur[0] != player_color:
        return False  # Kein Zug, weil keine eigene Figur bewegt wird.

    # **Eigene Figur darf nicht auf Zielfeld stehen**
    if board_state[row_2][column_2] and board_state[row_2][column_2][0] == player_color:
        return False  # Eigene Figur blockiert das Zielfeld

    figur_typ = figur[1]  # "P", "N", "B", "R", "Q", "K"

    if figur_typ == "P":  # Bauer
        return is_valid_pawn_move(board_state, start_position, target_position)
    elif figur_typ == "N":  # Springer
        return is_valid_knight_move(start_position, target_position)
    elif figur_typ == "B":  # Läufer
        return is_valid_bishop_move(board_state, start_position, target_position)
    elif figur_typ == "R":  # Turm
        return is_valid_rook_move(board_state, start_position, target_position)
    elif figur_typ == "Q":  # Dame
        return is_valid_queen_move(board_state, start_position, target_position)
    elif figur_typ == "K":  # König
        return is_valid_king_move(board_state, start_position, target_position)

    return False

def is_valid_pawn_move(board, start_position, target_position):
    row_1, column_1 = start_position
    row_2, column_2 = target_position
    direction = -1

    # Normaler Zug (eine Reihe nach vorne, kein Schlagen)
    if column_1 == column_2 and board[row_2][column_2] == "":
        if row_2 == row_1 + direction:
            return True  # 1 Feld nach vorne
        if (row_1 == 6): # Startposition prüfen
            if row_2 == row_1 + 2 * direction and board[row_1 + direction][column_1] == "":
                return True  # 2 Felder nach vorne (Startposition)
            
    # Schlagen (diagonal)
    if abs(column_2 - column_1) == 1 and row_2 == row_1 + direction:
        if board[row_2][column_2] and board[row_2][column_2][0]:
            return True  # Gegnerische Figur schlagen

    return False

def is_valid_knight_move(start_position, target_position):
    row_1, column_1 = start_position
    row_2, column_2 = target_position
    return (abs(row_2 - row_1), abs(column_2 - column_1)) in [(2, 1), (1, 2)]

def is_valid_bishop_move(board, start_position, target_position):
    row_1, column_1 = start_position
    row_1, column_2 = target_position
    if abs(row_1 - row_1) != abs(column_2 - column_1):  # Muss diagonal sein
        return False

    # Prüfe, ob der Weg frei ist
    schritt_r = 1 if row_1 > row_1 else -1
    schritt_s = 1 if column_2 > column_1 else -1
    r, s = row_1 + schritt_r, column_1 + schritt_s
    while (r, s) != (row_1, column_2):
        if board[r][s] != "":
            return False  # Blockiert
        r += schritt_r
        s += schritt_s

    return True

def is_valid_rook_move(board, start_position, target_position):
    row_1, column_1 = start_position
    row_2, column_2 = target_position
    if row_1 != row_2 and column_1 != column_2:  # Muss gerade Linie sein
        return False
    
    if row_1 == row_2 and column_1 == column_2: # Sein eigenes Feld
        return False

    schritt_r = 0 if row_1 == row_2 else (1 if row_2 > row_1 else -1)
    schritt_s = 0 if column_1 == column_2 else (1 if column_2 > column_1 else -1)
    r, s = row_1 + schritt_r, column_1 + schritt_s
    while (r, s) != (row_2, column_2):
        if board[r][s] != "":
            return False  # Blockiert
        r += schritt_r
        s += schritt_s

    return True

def is_valid_queen_move(board, start_position, target_position):
    return is_valid_bishop_move(board, start_position, target_position) or is_valid_rook_move(board, start_position, target_position)

def is_valid_king_move(start_position, target_position):
    row_1, column_1 = start_position
    row_2, column_2 = target_position
    
    if row_1 == row_2 and column_1 == column_2: # Sein eigenes Feld
        return False
    
    return abs(row_2 - row_1) <= 1 and abs(column_2 - column_1) <= 1  # 1 Feld in jede Richtung

# Funktion zur Drehung des Schachbretts für die KI
def drehe_schachbrett_fuer_ki(board, player_color):
    if player_color == "w":  # Wenn der Spieler schwarz ist, drehe das Schachbrett für die KI
        return [reihe[::-1] for reihe in board[::-1]]  # Umdrehen der Reihen und Spalten
    else:
        return board  # Andernfalls das Schachbrett unverändert lassen


def get_possible_moves(board, selected_position, current_player):
    possible_moves = []

    for r in range(8):
        for s in range(8):
            if is_valid_chess_move(board, selected_position, (r, s), current_player):
                possible_moves.append((r, s))

    return possible_moves



# Hauptfunktion
def main():
    global possible_positions
    screen = game.screen
    player_selected_color = game.get_select_player() # Auswahl der Farbe Spieler
    ki_selected_color = game.get_ki_selected_color(player_selected_color)  # Auswahl der Farbe KI
    board_state = board.get_array_board(player_selected_color)
    player_begin = game.player_begin_game

    feld_size = 80
    move_list = [] # Liste, um die Züge zu speichern
    selected_position = None
    move_count = 0
    king_death_position = None  # Variable zum Verfolgen der roten Markierung

    while True:
        for event in p.event.get():
            if event.type == p.QUIT:
                p.quit()
                sys.exit()
            if event.type == p.MOUSEBUTTONDOWN:
                mouse_x_position, mouse_y_position = p.mouse.get_pos()
                column = mouse_x_position // feld_size
                row = mouse_y_position // feld_size

                if 0 <= column < 8 and 0 <= row < 8:
                    if selected_position is None:
                        if board_state[row][column] and board_state[row][column][0] == player_begin:
                            selected_position = (row, column)
                    else:
                        target_row = row
                        target_column = column

                        if not is_valid_chess_move(board_state, selected_position, (target_row, target_column), player_begin):
                            #print("Ungültiger Zug!")
                            selected_position = None
                            possible_positions = []
                            continue

                        else:
                            figur = board_state[selected_position[0]][selected_position[1]]
                            move_list.append(f"{get_piece_name(figur)} von {chr(selected_position[1] + 65)}{8 - selected_position[0]} nach {chr(target_column + 65)}{8 - target_row}")

                            board_state[target_row][target_column] = figur
                            board_state[selected_position[0]][selected_position[1]] = ""

                            # Check to converting
                            if figur[1] == "P" and (target_row == 0 or target_row == 7):
                                neue_figur = bauernumwandlung(screen, player_begin)
                                figuren_map = {"Dame": "Q", "Turm": "R", "Springer": "N", "Läufer": "B"}
                                board_state[target_row][target_column] = player_begin + figuren_map[neue_figur]

                            selected_position = None

                            # Prüfen, ob der gegnerische König geschlagen wurde
                            if win_state(board_state, player_begin):
                                # Das Spiel ist gewonnen, zeige den Gewinner
                                screen.fill((240, 217, 181))  # Hintergrund zurücksetzen
                                render_chess_game(screen, board_state, feld_size, selected_position, king_death_position)
                                render_move_history(screen, move_list)

                                game.set_text((f"Spieler {('Weiß' if player_begin == 'w' else 'Schwarz')} gewinnt!", 36, (0, 0, 0), False, 100, 250))
                                game.set_text(f"Züge: {move_count+1}", 24, (0, 0, 0), False, 250, 305)
                                game.set_text("Möchtest du nochmal spielen? (J/N)", 24,(0, 0, 0), False, 100, 345)
                                p.display.flip()

                                warten = True
                                while warten:
                                    for event in p.event.get():
                                        if event.type == p.QUIT:
                                            p.quit()
                                            sys.exit()
                                        if event.type == p.KEYDOWN:
                                            if event.key == p.K_j:  # Wenn 'J' für Ja gedrückt wird
                                                main()  # Neue Runde starten
                                            elif event.key == p.K_n:  # Wenn 'N' für Nein gedrückt wird
                                                p.quit()  # Spiel beenden
                                                sys.exit()
                                return  # Funktion verlassen, um das Spiel zu beenden

                            # Wechseln des Zuges
                            player_begin = "w" if player_begin == "b" else "b"
                            move_count += 1

                # KI am Zug
                if player_begin == ki_selected_color:
                    #print(board_state) #todo: hier bist du :)
                    # Aktuelles Brett an Stockfish übergeben
                    board_state = drehe_schachbrett_fuer_ki(board_state, player_begin)
                    #print(board_state)
                    rochade_rechte = calculate_castling_rights(board_state, move_list)
                    en_passant_feld = calculate_en_passant_square(move_list)

                    stockfish.set_fen_position(
                        convert_board_to_fen(board_state, player_begin, rochade_rechte, en_passant_feld, move_count)
                    )

                    ki_zug = stockfish.get_best_move()

                    # KI-Zug umsetzen
                    start_pos, ziel_pos = ki_zug[:2], ki_zug[2:]
                    start_reihe, start_spalte = 8 - int(start_pos[1]), ord(start_pos[0].lower()) - ord('a')
                    target_row, target_column = 8 - int(ziel_pos[1]), ord(ziel_pos[0].lower()) - ord('a')

                    #print(start_reihe, target_row, start_spalte, ziel_spalte)
                    #print(f"Start-Spalte berechnet: {start_spalte}, Zeichen: {start_pos[0]}")
                    #print(f"Ziel-Spalte berechnet: {ziel_spalte}, Zeichen: {ziel_pos[0]}")
                    #print(f"KI-Zug: {ki_zug}")  # Debug-Ausgabe
                    #print(f"Start: {start_pos}, Ziel: {ziel_pos}")
                    #print(f"Start-Koordinaten: Reihe={start_reihe}, Spalte={start_spalte}")
                    #print(f"Ziel-Koordinaten: Reihe={target_row}, Spalte={ziel_spalte}")

                    figur = board_state[start_reihe][start_spalte]
                    move_list.append(f"{get_piece_name(figur)} von {start_pos[0].upper()}{start_pos[1]} nach {ziel_pos[0].upper()}{ziel_pos[1]}")

                    board_state[target_row][target_column] = figur
                    board_state[start_reihe][start_spalte] = ""

                    board_state = drehe_schachbrett_fuer_ki(board_state, player_begin)

                    # Spielerzug wechseln
                    player_begin = "w" if player_begin == "b" else "b"
                    move_count += 1

        # Schachbrett und andere Informationen zeichnen
        screen.fill((240, 217, 181))
        possible_positions = [] if selected_position is None else get_possible_moves(board_state, selected_position, player_begin)
        render_chess_game(screen, board_state, feld_size, selected_position, possible_positions, king_death_position)
        render_move_history(screen, move_list)
        game.set_text( f"Spieler: {'Weiß' if player_begin == 'w' else 'Schwarz'} ist dran!", 30, (0,0,0), False, 675, 580)
        p.display.flip()
        game.set_clock_time(30)


if __name__ == "__main__":
    main()