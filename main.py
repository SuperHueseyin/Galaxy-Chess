import pygame as p
import sys
from stockfish import Stockfish

# Initialisiere Stockfish
stockfish = Stockfish(path="stockfish/stockfish-windows-x86-64-sse41-popcnt.exe", parameters={"Threads": 2, "Skill Level": 10})


# p initialisieren
def initialisiere_p():
    p.init()
    screen = p.display.set_mode((1080, 640))  # Fenstergröße erweitert
    p.display.set_caption("Schachbrett")
    return screen

# Text auf den Bildschirm rendern
def zeichne_text(screen, text, font_size, x, y, farbe):
    font = p.font.SysFont("Arial", font_size, True)
    text_surface = font.render(text, True, farbe)
    screen.blit(text_surface, (x, y))

# Auswahl für den Spieler mit Buttons
def spieler_auswahl(screen):
    screen.fill((220, 197, 161))  # Hintergrundfarbe

    # Text für die Frage zentrieren
    font = p.font.SysFont("Arial", 36, True)
    text_surface = font.render("Wähle deine Farbe:", True, (0, 0, 0))
    text_rect = text_surface.get_rect(center=(screen.get_width() // 2, 250))
    screen.blit(text_surface, text_rect)

    # Buttons definieren
    weiß_button = p.Rect((screen.get_width() // 2) - 210, 280, 200, 80)  # Weiß Button
    schwarz_button = p.Rect((screen.get_width() // 2) + 0, 280, 200, 80)  # Schwarz Button

    # Weiß-Button zeichnen
    p.draw.rect(screen, (255, 255, 255), weiß_button)  # Weißer Button
    weiß_text = font.render("Weiß", True, (0, 0, 0))
    weiß_text_rect = weiß_text.get_rect(center=weiß_button.center)
    screen.blit(weiß_text, weiß_text_rect)

    # Schwarz-Button zeichnen
    p.draw.rect(screen, (0, 0, 0), schwarz_button)  # Schwarzer Button
    schwarz_text = font.render("Schwarz", True, (255, 255, 255))
    schwarz_text_rect = schwarz_text.get_rect(center=schwarz_button.center)
    screen.blit(schwarz_text, schwarz_text_rect)

    p.display.flip()

    # Event-Schleife für die Auswahl
    while True:
        for event in p.event.get():
            if event.type == p.QUIT:
                p.quit()
                sys.exit()

            if event.type == p.MOUSEBUTTONDOWN:
                maus_x, maus_y = p.mouse.get_pos()

                if weiß_button.collidepoint(maus_x, maus_y):
                    return "w"  # Spieler wählt Weiß
                elif schwarz_button.collidepoint(maus_x, maus_y):
                    return "b"  # Spieler wählt Schwarz

# Übersetzt die Abkürzungen der Figuren in Namen
def figur_name(figur):
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
    return namen.get(figur, "Unbekannt")

# Ein Schachbrett zeichnen
def zeichne_schachbrett(screen, schachbrett, feld_size, ausgewählt, schlag_koenig_position=None):
    farbe_hell = (240, 217, 181)  # Hellbraun
    farbe_dunkel = (181, 136, 99)  # Dunkelbraun
    farbe_auswahl = (255, 215, 0)  # Gold für Auswahl
    farbe_rot = (255, 0, 0)  # Rot für das Feld unter dem König

    figur_bilder = {
        "bR": p.image.load("images1/bR.png"),
        "bN": p.image.load("images1/bN.png"),
        "bB": p.image.load("images1/bB.png"),
        "bQ": p.image.load("images1/bQ.png"),
        "bK": p.image.load("images1/bK.png"),
        "bP": p.image.load("images1/bP.png"),
        "wR": p.image.load("images1/wR.png"),
        "wN": p.image.load("images1/wN.png"),
        "wB": p.image.load("images1/wB.png"),
        "wQ": p.image.load("images1/wQ.png"),
        "wK": p.image.load("images1/wK.png"),
        "wP": p.image.load("images1/wP.png")
    }

    for key in figur_bilder:
        figur_bilder[key] = p.transform.scale(figur_bilder[key], (feld_size, feld_size))

    # Schachbrett zeichnen
    for reihe in range(8):
        for spalte in range(8):
            if (reihe + spalte) % 2 == 0:
                farbe = farbe_hell
            else:
                farbe = farbe_dunkel

            if ausgewählt == (reihe, spalte):
                farbe = farbe_auswahl

            # Wenn das Feld unter dem König geschlagen wurde, färbe es rot
            if schlag_koenig_position and schlag_koenig_position == (reihe, spalte):
                farbe = farbe_rot

            p.draw.rect(screen, farbe, p.Rect(spalte * feld_size, reihe * feld_size, feld_size, feld_size))

            figur = schachbrett[reihe][spalte]
            if figur:
                screen.blit(figur_bilder[figur], (spalte * feld_size, reihe * feld_size))

# Textfeld für Züge zeichnen
def zeichne_zug_liste(screen, zug_liste):
    text_rect = p.Rect(660, 10, 400, 620)  # Bereich des Textfelds
    p.draw.rect(screen, (181, 126, 79), text_rect)  # Hintergrundfarbe

    # Maximal 20 Züge anzeigen (nur die letzten)
    max_anzahl = 20
    letzte_zuege = zug_liste[-max_anzahl:]  # Nur die letzten X Züge holen

    # Züge anzeigen
    font = p.font.SysFont("Arial", 25)
    y_offset = 20  # Abstand zum oberen Rand des Textfelds
    for i, zug in enumerate(letzte_zuege, start=max(1, len(zug_liste) - max_anzahl + 1)):
        zeichne_text(screen, f"{i}. {zug}", 20, 670, y_offset, (0, 0, 0))
        y_offset += 25  # Abstand zwischen den Einträgen

# Auswahlmenü für Umwandlung
def bauernumwandlung(screen, farbe):
    screen.fill((220, 197, 161))  # Hintergrundfarbe

    font = p.font.SysFont("Arial", 36, True)
    zeichne_text(screen, "Wähle die neue Figur:", 36, 360, 100, (0, 0, 0))

    if farbe == "w":  # Weißer Spieler
        figuren = ["Dame", "Turm", "Springer", "Läufer"]
        figuren_bilder = {
            "Dame": p.image.load("images1/wQ.png"),  # Weiße Dame Bild
            "Turm": p.image.load("images1/wR.png"),  # Weißer Turm Bild
            "Springer": p.image.load("images1/wN.png"),  # Weißer Springer Bild
            "Läufer": p.image.load("images1/wB.png")   # Weißer Läufer Bild
        }
    else:  # Schwarzer Spieler
        figuren = ["Dame", "Turm", "Springer", "Läufer"]
        figuren_bilder = {
            "Dame": p.image.load("images1/bQ.png"),  # Schwarze Dame Bild
            "Turm": p.image.load("images1/bR.png"),  # Schwarzer Turm Bild
            "Springer": p.image.load("images1/bN.png"),  # Schwarzer Springer Bild
            "Läufer": p.image.load("images1/bB.png")   # Schwarzer Läufer Bild
        }
    
    # Bildgröße anpassen (für die Darstellung im Menü)
    bild_size = (60, 60)
    for key in figuren_bilder:
        figuren_bilder[key] = p.transform.scale(figuren_bilder[key], bild_size)

    buttons = []
    for i, figur in enumerate(figuren):
        button = p.Rect(370, 200 + i * 100, 200, 60)
        buttons.append((button, figur))
        
        # Rechteck für den Button zeichnen
        p.draw.rect(screen, (0, 0, 0), button)
        
        # Text anzeigen
        text_color = (255, 255, 255)
        zeichne_text(screen, figur, 30, button.x + 50, button.y + 15, text_color)
        
        # Bild anzeigen
        screen.blit(figuren_bilder[figur], (button.x + 200, button.y + 0))

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

# Überprüft, ob der gegnerische König geschlagen wurde
def ist_gewonnen(schachbrett, spieler_am_zug):
    gegner_farbe = "b" if spieler_am_zug == "w" else "w"
    for reihe in range(8):
        for spalte in range(8):
            if schachbrett[reihe][spalte] == f"{gegner_farbe}K":
                return False  # Der gegnerische König ist noch auf dem Brett

    return True  # Der gegnerische König wurde geschlagen

# Funktion zur Umwandlung eines Bauern
def baue_um(schachbrett, spieler_am_zug, reihe, spalte):
    if (spieler_am_zug == 'w' and reihe == 0) or (spieler_am_zug == 'b' and reihe == 7):
        # Umwandlung zu Dame
        schachbrett[reihe][spalte] = f"{spieler_am_zug}Q"
        
#
#neu von mir
#
def convertiere_schachbrett_zu_fen(schachbrett, spieler_am_zug, rochade_rechte, en_passant_feld, zug_nummer):
    """
    Konvertiert das Schachbrett in das FEN-Format.
    :param schachbrett: 2D-Liste mit Figuren (z. B. "wP", "bK", "", etc.)
    :param spieler_am_zug: "w" oder "b", je nachdem, welcher Spieler am Zug ist
    :param rochade_rechte: String, z. B. "KQkq", gibt Rochade-Möglichkeiten an
    :param en_passant_feld: En-Passant-Feld, z. B. "e3", oder "-" falls nicht möglich
    :param zug_nummer: Aktuelle Zugnummer
    :return: String im FEN-Format
    """
    fen = ""

    # 1. Spielfeld in FEN umwandeln
    for reihe in schachbrett:
        leere_felder = 0
        for feld in reihe:
            if feld == "":
                leere_felder += 1
            else:
                if leere_felder > 0:
                    fen += str(leere_felder)
                    leere_felder = 0
                fen += feld[1].upper() if feld[0] == "w" else feld[1].lower()
        if leere_felder > 0:
            fen += str(leere_felder)
        fen += "/"
    fen = fen[:-1]  # Entferne den letzten Slash

    # 2. Spieler am Zug
    fen += f" {spieler_am_zug} "

    # 3. Rochaderechte
    fen += rochade_rechte if rochade_rechte else "-"

    # 4. En-Passant-Feld
    fen += f" {en_passant_feld} "

    # 5. Halbzüge (für 50-Züge-Regel, aktuell auf 0 gesetzt, falls nicht gespeichert)
    fen += "0 "

    # 6. Zugnummer
    fen += str(zug_nummer)

    return fen

def berechne_rochade_rechte(schachbrett, zug_liste):
    rochade_rechte = ""

    # Prüfen, ob sich der weiße König oder Türme bewegt haben
    if "wK" in schachbrett[7][4]:
        if "wR" in schachbrett[7][7] and "Ke1 nach h1" not in zug_liste:
            rochade_rechte += "K"
        if "wR" in schachbrett[7][0] and "Ke1 nach a1" not in zug_liste:
            rochade_rechte += "Q"

    # Prüfen, ob sich der schwarze König oder Türme bewegt haben
    if "bK" in schachbrett[0][4]:
        if "bR" in schachbrett[0][7] and "Ke8 nach h8" not in zug_liste:
            rochade_rechte += "k"
        if "bR" in schachbrett[0][0] and "Ke8 nach a8" not in zug_liste:
            rochade_rechte += "q"

    return rochade_rechte if rochade_rechte else "-"

def berechne_en_passant_feld(zug_liste):
    if not zug_liste:
        return "-"

    letzter_zug = zug_liste[-1]  # Letzten Zug holen, z. B. "Bauer von E2 nach E4"
    teile = letzter_zug.split()   # Zerlegen: ["Bauer", "von", "E2", "nach", "E4"]

    if "Bauer" in teile and "von" in teile and "nach" in teile:
        start_pos = teile[2]  # E2
        ziel_pos = teile[4]   # E4

        if len(start_pos) == 2 and len(ziel_pos) == 2:
            start_spalte, start_zeile = start_pos[0], int(start_pos[1])
            ziel_spalte, ziel_zeile = ziel_pos[0], int(ziel_pos[1])

            if abs(start_zeile - ziel_zeile) == 2:  # Bauer ist 2 Felder gezogen
                en_passant_feld = start_spalte + str((start_zeile + ziel_zeile) // 2)
                return en_passant_feld.lower()  # FEN benötigt Kleinbuchstaben für Spalten

    return "-"

def ist_zug_erlaubt(schachbrett, start, ziel, spieler_farbe):
    """
    Prüft, ob der Zug von `start` nach `ziel` für die aktuelle `spieler_farbe` erlaubt ist.
    """
    reihe1, spalte1 = start
    reihe2, spalte2 = ziel
    figur = schachbrett[reihe1][spalte1]

    if not figur or figur[0] != spieler_farbe:
        return False  # Kein Zug, weil keine eigene Figur bewegt wird.

    figur_typ = figur[1]  # "P", "N", "B", "R", "Q", "K"

    if figur_typ == "P":  # Bauer
        return ist_bauer_zug_erlaubt(schachbrett, start, ziel, spieler_farbe)
    elif figur_typ == "N":  # Springer
        return ist_springer_zug_erlaubt(start, ziel)
    elif figur_typ == "B":  # Läufer
        return ist_laeufer_zug_erlaubt(schachbrett, start, ziel)
    elif figur_typ == "R":  # Turm
        return ist_turm_zug_erlaubt(schachbrett, start, ziel)
    elif figur_typ == "Q":  # Dame
        return ist_dame_zug_erlaubt(schachbrett, start, ziel)
    elif figur_typ == "K":  # König
        return ist_koenig_zug_erlaubt(schachbrett, start, ziel)

    return False

def ist_bauer_zug_erlaubt(schachbrett, start, ziel, spieler_farbe):
    reihe1, spalte1 = start
    reihe2, spalte2 = ziel
    richtung = -1 if spieler_farbe == "w" else 1  # Weiße Bauern (-1), schwarze Bauern (+1)

    # Normaler Zug (eine Reihe nach vorne, kein Schlagen)
    if spalte1 == spalte2 and schachbrett[reihe2][spalte2] == "":
        if reihe2 == reihe1 + richtung:
            return True  # 1 Feld nach vorne
        # Startposition prüfen (weiße Bauern bei Reihe 6, schwarze bei Reihe 1)
        if (reihe1 == 6 and spieler_farbe == "w") or (reihe1 == 1 and spieler_farbe == "b"):
            if reihe2 == reihe1 + 2 * richtung and schachbrett[reihe1 + richtung][spalte1] == "":
                return True  # 2 Felder nach vorne (Startposition)

    # Schlagen (diagonal)
    if abs(spalte2 - spalte1) == 1 and reihe2 == reihe1 + richtung:
        if schachbrett[reihe2][spalte2] and schachbrett[reihe2][spalte2][0] != spieler_farbe:
            return True  # Gegnerische Figur schlagen

    return False


def ist_springer_zug_erlaubt(start, ziel):
    reihe1, spalte1 = start
    reihe2, spalte2 = ziel
    return (abs(reihe2 - reihe1), abs(spalte2 - spalte1)) in [(2, 1), (1, 2)]

def ist_laeufer_zug_erlaubt(schachbrett, start, ziel):
    reihe1, spalte1 = start
    reihe2, spalte2 = ziel
    if abs(reihe2 - reihe1) != abs(spalte2 - spalte1):  # Muss diagonal sein
        return False

    # Prüfe, ob der Weg frei ist
    schritt_r = 1 if reihe2 > reihe1 else -1
    schritt_s = 1 if spalte2 > spalte1 else -1
    r, s = reihe1 + schritt_r, spalte1 + schritt_s
    while (r, s) != (reihe2, spalte2):
        if schachbrett[r][s] != "":
            return False  # Blockiert
        r += schritt_r
        s += schritt_s

    return True

def ist_turm_zug_erlaubt(schachbrett, start, ziel):
    reihe1, spalte1 = start
    reihe2, spalte2 = ziel
    if reihe1 != reihe2 and spalte1 != spalte2:  # Muss gerade Linie sein
        return False

    schritt_r = 0 if reihe1 == reihe2 else (1 if reihe2 > reihe1 else -1)
    schritt_s = 0 if spalte1 == spalte2 else (1 if spalte2 > spalte1 else -1)
    r, s = reihe1 + schritt_r, spalte1 + schritt_s
    while (r, s) != (reihe2, spalte2):
        if schachbrett[r][s] != "":
            return False  # Blockiert
        r += schritt_r
        s += schritt_s

    return True

def ist_dame_zug_erlaubt(schachbrett, start, ziel):
    return ist_laeufer_zug_erlaubt(schachbrett, start, ziel) or ist_turm_zug_erlaubt(schachbrett, start, ziel)

def ist_koenig_zug_erlaubt(schachbrett, start, ziel):
    reihe1, spalte1 = start
    reihe2, spalte2 = ziel
    return abs(reihe2 - reihe1) <= 1 and abs(spalte2 - spalte1) <= 1  # 1 Feld in jede Richtung


#
#Ende neu von mir
#

# Hauptfunktion
def main():
    screen = initialisiere_p()
    clock = p.time.Clock()
    feld_size = 80
    zug_liste = []  # Liste, um die Züge zu speichern
    spieler_farbe = spieler_auswahl(screen)  # Auswahl der Farbe Spieler
    ki_farbe = "b" if spieler_farbe == "w" else "w" # Auswahl der Farbe KI


    if spieler_farbe == "w":
        schachbrett = [
            ["bR", "bN", "bB", "bQ", "bK", "bB", "bN", "bR"],
            ["bP" for _ in range(8)],
            ["" for _ in range(8)],
            ["" for _ in range(8)],
            ["" for _ in range(8)],
            ["" for _ in range(8)],
            ["wP" for _ in range(8)],
            ["wR", "wN", "wB", "wQ", "wK", "wB", "wN", "wR"]
        ]
        spieler_am_zug = "w"
    else:
        schachbrett = [
            ["wR", "wN", "wB", "wQ", "wK", "wB", "wN", "wR"],
            ["wP" for _ in range(8)],
            ["" for _ in range(8)],
            ["" for _ in range(8)],
            ["" for _ in range(8)],
            ["" for _ in range(8)],
            ["bP" for _ in range(8)],
            ["bR", "bN", "bB", "bQ", "bK", "bB", "bN", "bR"]
        ]
        spieler_am_zug = "w"

    ausgewählt = None
    zug_nummer = 0
    schlag_koenig_position = None  # Variable zum Verfolgen der roten Markierung

    while True:
        for event in p.event.get():
            if event.type == p.QUIT:
                p.quit()
                sys.exit()

            if event.type == p.MOUSEBUTTONDOWN:
                maus_x, maus_y = p.mouse.get_pos()
                spalte = maus_x // feld_size
                reihe = maus_y // feld_size

                if 0 <= spalte < 8 and 0 <= reihe < 8:
                    if ausgewählt is None:
                        if schachbrett[reihe][spalte] and schachbrett[reihe][spalte][0] == spieler_am_zug:
                            ausgewählt = (reihe, spalte)
                    else:
                        ziel_reihe, ziel_spalte = reihe, spalte

                        if not ist_zug_erlaubt(schachbrett, ausgewählt, (ziel_reihe, ziel_spalte), spieler_am_zug):
                            print("Ungültiger Zug!")  # Debugging
                            ausgewählt = None
                            continue  # Zurück zum Event-Loop

                        else:
                            figur = schachbrett[ausgewählt[0]][ausgewählt[1]]
                            zug_liste.append(f"{figur_name(figur)} von {chr(ausgewählt[1] + 65)}{8 - ausgewählt[0]} nach {chr(ziel_spalte + 65)}{8 - ziel_reihe}")

                            # Schlagen des Königs
                            if schachbrett[ziel_reihe][ziel_spalte] == f"{'b' if spieler_am_zug == 'w' else 'w'}K":
                                schlag_koenig_position = (ziel_reihe, ziel_spalte)

                            schachbrett[ziel_reihe][ziel_spalte] = figur
                            schachbrett[ausgewählt[0]][ausgewählt[1]] = ""

                            # Prüfen auf Umwandlung
                            if figur[1] == "P" and (ziel_reihe == 0 or ziel_reihe == 7):
                                neue_figur = bauernumwandlung(screen, spieler_am_zug)
                                figuren_map = {"Dame": "Q", "Turm": "R", "Springer": "N", "Läufer": "B"}
                                schachbrett[ziel_reihe][ziel_spalte] = spieler_am_zug + figuren_map[neue_figur]

                            ausgewählt = None

                            # Prüfen, ob der gegnerische König geschlagen wurde
                            if ist_gewonnen(schachbrett, spieler_am_zug):
                                # Das Spiel ist gewonnen, zeige den Gewinner
                                screen.fill((240, 217, 181))  # Hintergrund zurücksetzen
                                zeichne_schachbrett(screen, schachbrett, feld_size, ausgewählt, schlag_koenig_position)
                                zeichne_zug_liste(screen, zug_liste)

                                zeichne_text(screen, f"Spieler {('Weiß' if spieler_am_zug == 'w' else 'Schwarz')} gewinnt!", 36, 100, 250, (0, 0, 0))
                                zeichne_text(screen, f"Züge: {zug_nummer+1}", 24, 250, 305, (0, 0, 0))
                                zeichne_text(screen, "Möchtest du nochmal spielen? (J/N)", 24, 100, 345, (0, 0, 0))
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
                            spieler_am_zug = "w" if spieler_am_zug == "b" else "b"
                            zug_nummer += 1

        # KI am Zug
        if spieler_am_zug == ki_farbe:
            # Aktuelles Brett an Stockfish übergeben
            
            rochade_rechte = berechne_rochade_rechte(schachbrett, zug_liste)
            en_passant_feld = berechne_en_passant_feld(zug_liste)

            stockfish.set_fen_position(
                convertiere_schachbrett_zu_fen(schachbrett, spieler_am_zug, rochade_rechte, en_passant_feld, zug_nummer)
            )


            ki_zug = stockfish.get_best_move()

            # KI-Zug umsetzen
            start_pos, ziel_pos = ki_zug[:2], ki_zug[2:]
           # start_reihe, start_spalte = 8 - int(start_pos[1]), ord(start_pos[0]) - 65
            start_reihe, start_spalte = 8 - int(start_pos[1]), ord(start_pos[0].lower()) - ord('a')
           # ziel_reihe, ziel_spalte = 8 - int(ziel_pos[1]), ord(ziel_pos[0]) - 65
            ziel_reihe, ziel_spalte = 8 - int(ziel_pos[1]), ord(ziel_pos[0].lower()) - ord('a')

            print(f"Start-Spalte berechnet: {start_spalte}, Zeichen: {start_pos[0]}")
            print(f"Ziel-Spalte berechnet: {ziel_spalte}, Zeichen: {ziel_pos[0]}")

            
            print(f"KI-Zug: {ki_zug}")  # Debug-Ausgabe
            print(f"Start: {start_pos}, Ziel: {ziel_pos}")
            print(f"Start-Koordinaten: Reihe={start_reihe}, Spalte={start_spalte}")
            print(f"Ziel-Koordinaten: Reihe={ziel_reihe}, Spalte={ziel_spalte}")

            
            figur = schachbrett[start_reihe][start_spalte]
            zug_liste.append(f"{figur_name(figur)} von {start_pos} nach {ziel_pos}")

            schachbrett[ziel_reihe][ziel_spalte] = figur
            schachbrett[start_reihe][start_spalte] = ""

            # Prüfen auf Umwandlung
            if figur[1] == "P" and (ziel_reihe == 0 or ziel_reihe == 7):
                schachbrett[ziel_reihe][ziel_spalte] = f"{ki_farbe}Q"  # Automatisch Dame
            
            if ist_gewonnen(schachbrett, spieler_am_zug):
                ...

            # Spielerzug wechseln
            spieler_am_zug = "w" if spieler_am_zug == "b" else "b"
            zug_nummer += 1

        # Schachbrett und andere Informationen zeichnen
        screen.fill((240, 217, 181))
        zeichne_schachbrett(screen, schachbrett, feld_size, ausgewählt, schlag_koenig_position)
        zeichne_zug_liste(screen, zug_liste)
        zeichne_text(screen, f"Spieler: {'Weiß' if spieler_am_zug == 'w' else 'Schwarz'} ist dran!", 30, 675, 580, (0, 0, 0))
        p.display.flip()
        clock.tick(30)


if __name__ == "__main__":
    main()