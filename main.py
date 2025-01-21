import pygame as p
import sys
from stockfish import Stockfish

stockfish = Stockfish("/stockfish")
stockfish.set_skill_level(10)  # Passe die Schwierigkeit der KI an

ausgewaehltes_feld = None
spieler_am_zug = "w"  # "w" für Weiß, "b" für Schwarz


# p initialisieren
def initialisiere_p():
    p.init()
    screen = p.display.set_mode((1000, 640))  # Fenstergröße
    p.display.set_caption("Schachbrett")
    return screen

# Ein Schachbrett zeichnen
def zeichne_schachbrett(screen, schachbrett):
    farbe_hell = (240, 217, 181)  # Hellbraun
    farbe_dunkel = (181, 136, 99)  # Dunkelbraun

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

    feld_size = 80
    
    for key in figur_bilder:
        figur_bilder[key] = p.transform.scale(figur_bilder[key], (feld_size, feld_size))

    for reihe in range(8):
        for spalte in range(8):
            # Abwechselnde Farben für die Felder
            if (reihe + spalte) % 2 == 0:
                farbe = farbe_hell
            else:
                farbe = farbe_dunkel

            # Rechteck für das Feld zeichnen
            p.draw.rect(screen, farbe, p.Rect(spalte * feld_size, reihe * feld_size, feld_size, feld_size))

            # Figur auf das Feld zeichnen, falls vorhanden
            figur = schachbrett[reihe][spalte]
            if figur:
                screen.blit(figur_bilder[figur], (spalte * feld_size, reihe * feld_size))

# Hauptfunktion für das Schachbrett
def main():
    screen = initialisiere_p()
    clock = p.time.Clock()

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

    while True:
        for event in p.event.get():
            if event.type == p.QUIT:
                p.quit()
                sys.exit()

            # Spielerzug mit Maus
            elif event.type == p.MOUSEBUTTONDOWN and spieler_am_zug == "w":
                pos = p.mouse.get_pos()
                spalte, reihe = pos[0] // 80, pos[1] // 80

                if ausgewaehltes_feld:  # Ziehen
                    ziel = (reihe, spalte)
                    start = ausgewaehltes_feld
                    figur = schachbrett[start[0]][start[1]]

                    # Überprüfen, ob der Zug legal ist
                    zug = f"{chr(start[1] + 97)}{8 - start[0]}{chr(ziel[1] + 97)}{8 - ziel[0]}"
                    stockfish.set_position([zug])

                    if stockfish.is_move_correct(zug):  # Zug ausführen
                        schachbrett[start[0]][start[1]] = ""
                        schachbrett[ziel[0]][ziel[1]] = figur
                        spieler_am_zug = "b"  # Nächster Zug gehört der KI

                    ausgewaehltes_feld = None
                else:
                    ausgewaehltes_feld = (reihe, spalte)

        # Zug der KI
        if spieler_am_zug == "b":
            stockfish.set_position([f"{chr(c + 97)}{8 - r}" for r in range(8) for c in range(8) if schachbrett[r][c]])
            ki_zug = stockfish.get_best_move()

            if ki_zug:
                start = (8 - int(ki_zug[1]), ord(ki_zug[0]) - 97)
                ziel = (8 - int(ki_zug[3]), ord(ki_zug[2]) - 97)
                schachbrett[ziel[0]][ziel[1]] = schachbrett[start[0]][start[1]]
                schachbrett[start[0]][start[1]] = ""
                spieler_am_zug = "w"  # Nächster Zug gehört dem Spieler

        # Bildschirm aktualisieren
        screen.fill((240, 217, 181))
        zeichne_schachbrett(screen, schachbrett)
        p.display.flip()
        clock.tick(30)


if __name__ == "__main__":
    main()
