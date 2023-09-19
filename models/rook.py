import pygame

from models.figure import Figure


class Rook(Figure):
    picture_white = pygame.image.load('img/rook.png')
    picture_black = pygame.image.load('img/black_rook.png')
    type = "rook"

    def calculate_moves(self):
        possible_moves = [
            self.moves_right(),
            self.moves_left(),
            self.moves_up(),
            self.moves_down()
        ]
        return possible_moves

    def __repr__(self):
        return f"Rook_Object_at_{self.x} /{self.y}"
