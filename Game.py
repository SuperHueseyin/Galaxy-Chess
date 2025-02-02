import pygame as game

class Game:
    def __init__(self, width=1080, height=640, title="Schachbrett"):
        self.font = None
        self.mouse_pos_x = None
        self.mouse_pos_y = None
        self.screen = game.display.set_mode((width, height))
        self.player_begin_game= "w"
        game.init()
        game.display.set_caption(title)

    def set_clock_time(self, time):
        self.get_clock().tick(time)

    def get_clock(self):
        return game.time.Clock()

    def get_screen(self):
        return self.screen

    def get_sys_font(self, size):
        self.font = game.font.SysFont("Arial", size, True)
        return self.font

    def get_text(self):
        pass

    def set_text(self, text, font_size, color, center, *args):
        text_surface = self.get_sys_font(font_size).render(text, True, color)
        if not center:
            self.screen.blit(text_surface, args)
        else:
            text_rect = text_surface.get_rect(center=args)
            self.screen.blit(text_surface, text_rect)

    def get_button(self, x_pos, y_pos, width, height):
        button = game.Rect(x_pos, y_pos, width, height)
        return button

    def get_ki_selected_color(self, player_color):
        return "b" if player_color == "w" else "w"

    def get_select_player(self):
        self.screen.fill((220, 197, 161))

        # Ask player for select color
        self.set_text("Wähle deine Farbe:", 36, (0,0,0), True, (self.screen.get_width() // 2, 250))

        # Buttons define
        weiß_button = self.get_button((self.screen.get_width() // 2) - 210, 280, 200, 80)  # Weiß Button
        schwarz_button = self.get_button((self.screen.get_width() // 2) + 0, 280, 200, 80)  # Schwarz Button

        # White button define
        game.draw.rect(self.screen, (255,255,255), weiß_button)
        self.set_text("Weiß",36, (0,0,0), True, weiß_button.center)

        # Black button define
        game.draw.rect(self.screen, (0, 0, 0), schwarz_button)
        self.set_text("Schwarz",36, (255,255,255), True, schwarz_button.center)

        game.display.flip()

        return self.set_player_selected_button_color(schwarz_button, weiß_button)

    def set_player_selected_button_color(self, schwarz_button, weiß_button):
        while True:
            for event in game.event.get():
                if event.type == game.MOUSEBUTTONDOWN:
                    self.mouse_pos_x, self.mouse_pos_y = game.mouse.get_pos()
                    if weiß_button.collidepoint(self.mouse_pos_x, self.mouse_pos_y):
                        return "w"
                    elif schwarz_button.collidepoint(self.mouse_pos_x, self.mouse_pos_y):
                        return "b"