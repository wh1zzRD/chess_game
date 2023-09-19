import pygame

from models.figure import Figure


class Queen(Figure):
    picture_white = pygame.image.load('img/queen.png')
    picture_black = pygame.image.load('img/black_queen.png')
    type = "queen"

    def calculate_moves(self):
        possible_moves = [
            self.moves_right(),
            self.moves_left(),
            self.moves_up(),
            self.moves_down(),
            self.moves_up_right(),
            self.moves_up_left(),
            self.moves_down_right(),
            self.moves_down_left()
        ]
        return possible_moves

    def __repr__(self):
        return f"Queen_Object_at_{self.x}/{self.y}"
