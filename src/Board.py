from src.Figure import Figure
import pygame as game

class Board:
    def __init__(self, screen):
        self.field_color_light = (240, 217, 181)
        self.field_color_dark = (181, 136, 99)
        self.field_color_select_figure = (255, 215, 0)
        self.field_color_possible_position = (135, 206, 250)
        self.square_field_color_king_threat = (255, 0, 0)
        self.square_field_size = 80
        self.screen = screen
        self.board = None
        self.figure_dir = {}
        self.board = []
        self._load_figure_dir()
        self.move_list = []

    def _load_figure_dir(self):
        for figure in Figure:
            image = game.image.load(figure.img_path)
            scaled_image = game.transform.scale(image, (self.square_field_size, self.square_field_size))
            self.figure_dir[figure.short_name] = scaled_image

    def create_square_fields(self, selected_position, possible_position, king_threat_pos):
        for key in self.figure_dir:
            self.figure_dir[key] = game.transform.scale(self.figure_dir[key], (self.square_field_size, self.square_field_size))

        for row in range(8):
            for col in range(8):
                if (row + col) % 2 == 0:
                    color = self.field_color_light
                else:
                    color = self.field_color_dark

                if selected_position == (row, col):
                    color = self.field_color_select_figure

                if king_threat_pos and king_threat_pos == (row, col):
                    color = self.square_field_color_king_threat

                game.draw.rect(
                    self.screen,
                    color,
                    game.Rect(col * self.square_field_size, row * self.square_field_size, self.square_field_size, self.square_field_size)
                )

                figure = self.board[row][col]
                if figure:
                    #print(self.figure_dir[figure.short_name])
                    self.screen.blit(
                        self.figure_dir[figure.short_name],
                        (col * self.square_field_size, row * self.square_field_size)
                    )

                if possible_position and (row, col) in possible_position:
                    color = self.field_color_possible_position

    def set_figure_on_square_fields(self):
        for row in range(8):
            for col in range(8):
                piece = self.board[row][col]

                if piece:
                    self.screen.blit(
                        self.figure_dir[piece.short_name],
                        (col * self.square_field_size, row * self.square_field_size)
                    )

    def get_array_board(self, player_color):
        if player_color == "w":
            self.board = [
                ["bR", "bN", "bB", "bQ", "bK", "bB", "bN", "bR"],
                ["bP" for _ in range(8)],
                ["" for _ in range(8)],
                ["" for _ in range(8)],
                ["" for _ in range(8)],
                ["" for _ in range(8)],
                ["wP" for _ in range(8)],
                ["wR", "wN", "wB", "wQ", "wK", "wB", "wN", "wR"]
            ]

        if player_color == "b":
            self.board= [
                ["wR", "wN", "wB", "wQ", "wK", "wB", "wN", "wR"],
                ["wP" for _ in range(8)],
                ["" for _ in range(8)],
                ["" for _ in range(8)],
                ["" for _ in range(8)],
                ["" for _ in range(8)],
                ["bP" for _ in range(8)],
                ["bR", "bN", "bB", "bQ", "bK", "bB", "bN", "bR"]
            ]

        return self.board