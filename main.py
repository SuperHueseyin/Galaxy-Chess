import pygame as p
import sys

# p initialisieren
def initialisiere_p():
    p.init()
    screen = p.display.set_mode((1000, 640))  # Fenstergröße
    p.display.set_caption("Schachbrett")
    return screen

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

    feld_size = 80
    
    for key in figur_bilder:
        figur_bilder[key] = p.transform.scale(figur_bilder[key], (feld_size, feld_size))

    # Schachbrett zeichnen
    for reihe in range(8):
        for spalte in range(8):
            # Abwechselnde Farben für die Felder
            if (reihe + spalte) % 2 == 0:
                farbe = farbe_hell
            else:
                farbe = farbe_dunkel

            # Hervorheben, wenn das Feld ausgewählt ist
            if ausgewählt == (reihe, spalte):
                farbe = farbe_auswahl

            # Rechteck für das Feld zeichnen
            p.draw.rect(screen, farbe, p.Rect(spalte * feld_size, reihe * feld_size, feld_size, feld_size))

            # Figur auf das Feld zeichnen, falls vorhanden
            figur = schachbrett[reihe][spalte]
            if figur:
                screen.blit(figur_bilder[figur], (spalte * feld_size, reihe * feld_size))

# Hauptfunktion
def main():
    screen = initialisiere_p()
    clock = p.time.Clock()

    feld_size = 80  # Größe eines Feldes
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

    ausgewählt = None  # Speichert die aktuell ausgewählte Figur

    while True:
        for event in p.event.get():
            if event.type == p.QUIT:
                p.quit()
                sys.exit()

            if event.type == p.MOUSEBUTTONDOWN:
                maus_x, maus_y = p.mouse.get_pos()
                spalte = maus_x // feld_size
                reihe = maus_y // feld_size

                if 0 <= spalte < 8 and 0 <= reihe < 8:  # Klick innerhalb des Schachbretts
                    if ausgewählt is None:  # Noch nichts ausgewählt
                        if schachbrett[reihe][spalte]:  # Figur vorhanden
                            ausgewählt = (reihe, spalte)
                    else:  # Eine Figur ist bereits ausgewählt
                        ziel_reihe, ziel_spalte = reihe, spalte

                        # Figur bewegen
                        schachbrett[ziel_reihe][ziel_spalte] = schachbrett[ausgewählt[0]][ausgewählt[1]]
                        schachbrett[ausgewählt[0]][ausgewählt[1]] = ""
                        ausgewählt = None  # Auswahl zurücksetzen

        screen.fill((240,217,181))  # Hintergrund schwarz
        zeichne_schachbrett(screen, schachbrett, feld_size, ausgewählt)
        p.display.flip()
        clock.tick(30)

if __name__ == "__main__":
    main()