import pygame as p
import sys

# p initialisieren
def initialisiere_p():
    p.init()
    screen = p.display.set_mode((720, 720))  # Fenstergröße
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

    feld_size = 90
    
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

        screen.fill((0, 0, 0))  # Hintergrund schwarz
        zeichne_schachbrett(screen, schachbrett)
        p.display.flip()
        clock.tick(30)

if __name__ == "__main__":
    main()
