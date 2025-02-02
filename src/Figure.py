from enum import Enum

class Figure(Enum):
    KING_WHITE = ("wK", "Weißer König", "img/wK.png")
    KING_BLACK = ("bK", "Schwarzer König", "img/bK.png")

    QUEEN_WHITE = ("wQ", "Weiße Dame", "img/wQ.png")
    QUEEN_BLACK = ("bQ", "Schwarze Dame", "img/bQ.png")

    BISHOP_WHITE = ("wB", "Weißer Läufer", "img/wB.png")
    BISHOP_BLACK = ("bB", "Schwarzer Läufer", "img/bB.png")

    ROOK_WHITE = ("wR", "Weißer Turm", "img/wR.png")
    ROOK_BLACK = ("bR", "Schwarzer Turm", "img/bR.png")

    KNIGHT_WHITE = ("wK", "Weißer Springer", "img/wK.png")
    KNIGHT_BLACK = ("bK", "Schwarzer Springer", "img/bK.png")

    PAWN_WHITE = ("wP", "Weißer Bauer", "img/wP.png")
    PAWN_BLACK = ("bP", "Schwarzer Bauer", "img/bP.png")

    def __init__(self, short_name, full_name, img_path):
        self.short_name = short_name
        self.full_name = full_name
        self.img_path = img_path