import pygame as p
import sys

# p initialisieren
def initialisiere_p():
    p.init()
    screen = p.display.set_mode((1000, 640))  # Fenstergröße
    p.display.set_caption("Schachbrett")
    return screen

# Text auf den Bildschirm rendern
def zeichne_text(screen, text, font_size, x, y, farbe):
    font = p.font.SysFont("Arial", font_size, True)
    text_surface = font.render(text, True, farbe)
    screen.blit(text_surface, (x, y))

# Auswahl für den Spieler mit Buttons
def spieler_auswahl(screen):
    screen.fill((240, 217, 181))  # Hintergrundfarbe

    # Text für die Frage zentrieren
    font = p.font.SysFont("Arial", 36, True)
    text_surface = font.render("Wähle deine Farbe:", True, (0, 0, 0))
    text_rect = text_surface.get_rect(center=(screen.get_width() // 2, 200))
    screen.blit(text_surface, text_rect)

    # Buttons definieren
    weiß_button = p.Rect((screen.get_width() // 2) - 150, 300, 200, 80)  # Weiß Button
    schwarz_button = p.Rect((screen.get_width() // 2) + 50, 300, 200, 80)  # Schwarz Button

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

# Ein Schachbrett zeichnen
def zeichne_schachbrett(screen, schachbrett, feld_size, ausgewählt):
    farbe_hell = (240, 217, 181)  # Hellbraun
    farbe_dunkel = (181, 136, 99)  # Dunkelbraun
    farbe_auswahl = (255, 215, 0)  # Gold für Auswahl

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

            p.draw.rect(screen, farbe, p.Rect(spalte * feld_size, reihe * feld_size, feld_size, feld_size))

            figur = schachbrett[reihe][spalte]
            if figur:
                screen.blit(figur_bilder[figur], (spalte * feld_size, reihe * feld_size))

# Hauptfunktion
def main():
    screen = initialisiere_p()
    clock = p.time.Clock()
    feld_size = 80
    spieler_farbe = spieler_auswahl(screen)  # Auswahl der Farbe

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
        spieler_am_zug = "b"

    ausgewählt = None
    zug_nummer = 1

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

                        # Verhindern, dass Figuren derselben Farbe geschlagen werden
                        if schachbrett[ziel_reihe][ziel_spalte] and schachbrett[ziel_reihe][ziel_spalte][0] == spieler_am_zug:
                            ausgewählt = None  # Auswahl aufheben
                        else:
                            # Figur bewegen
                            schachbrett[ziel_reihe][ziel_spalte] = schachbrett[ausgewählt[0]][ausgewählt[1]]
                            schachbrett[ausgewählt[0]][ausgewählt[1]] = ""
                            ausgewählt = None

                            # Spielerwechsel und Zugnummer hochzählen
                            spieler_am_zug = "w" if spieler_am_zug == "b" else "b"
                            zug_nummer += 1

        screen.fill((240, 217, 181))  # Hintergrund
        zeichne_text(screen, f"Zug: {zug_nummer}, Spieler: {'Weiß' if spieler_am_zug == 'w' else 'Schwarz'}", 24, 10, 610, (0, 0, 0))
        zeichne_schachbrett(screen, schachbrett, feld_size, ausgewählt)
        p.display.flip()
        clock.tick(30)

if __name__ == "__main__":
    main()
