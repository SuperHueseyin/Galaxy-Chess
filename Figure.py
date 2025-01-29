from enum import Enum

class Figure(Enum):
    KING_WHITE = ("King", 1, "E1")
    KING_BLACK = ("King", 2, "E8")

    QUEEN_WHITE = ("Queen", 3, "D1")
    QUEEN_BLACK = ("Queen", 4, "D8")

    LAEUFER_WHITE_1 = ("Läufer", 5, "C1")
    LAEUFER_WHITE_2 = ("Läufer", 6, "F1")
    LAEUFER_BLACK_1 = ("Läufer", 7, "C8")
    LAEUFER_BLACK_2 = ("Läufer", 8, "F8")

    TURM_WHITE_1 = ("Turm", 9, "A1")
    TURM_WHITE_2 = ("Turm", 10, "H1")
    TURM_BLACK_1 = ("Turm", 11, "A8")
    TURM_BLACK_2 = ("Turm", 12, "H8")

    SPRINGER_WHITE_1 = ("Springer", 13, "B1")
    SPRINGER_WHITE_2 = ("Springer", 14, "G1")
    SPRINGER_BLACK_1 = ("Springer", 15, "B8")
    SPRINGER_BLACK_2 = ("Springer", 16, "G8")

    BAUER_BLACK_1 = ("Bauer", 17, "A7")
    BAUER_BLACK_2 = ("Bauer", 18, "B7")
    BAUER_BLACK_3 = ("Bauer", 19, "C7")
    BAUER_BLACK_4 = ("Bauer", 20, "D7")
    BAUER_BLACK_5 = ("Bauer", 21, "E7")
    BAUER_BLACK_6 = ("Bauer", 22, "F7")
    BAUER_BLACK_7 = ("Bauer", 23, "G7")
    BAUER_BLACK_8 = ("Bauer", 24, "H7")
    BAUER_WHITE_1 = ("Bauer", 25, "A2")
    BAUER_WHITE_2 = ("Bauer", 26, "B2")
    BAUER_WHITE_3 = ("Bauer", 27, "C2")
    BAUER_WHITE_4 = ("Bauer", 28, "D2")
    BAUER_WHITE_5 = ("Bauer", 29, "E2")
    BAUER_WHITE_6 = ("Bauer", 30, "F2")
    BAUER_WHITE_7 = ("Bauer", 31, "G2")
    BAUER_WHITE_8 = ("Bauer", 32, "H2")

    def __init__(self, figure_name, figure_id, figure_init_pos):
        self.figure_name = figure_name
        self.figure_id = figure_id
        self.figure_init_pos = figure_init_pos

    def __repr__(self):
        return (f"Sachfigur(name={self.figure_name}, id={self.figure_id}, "
                f"init_pos={self.figure_init_pos})")
