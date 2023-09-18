import pygame

from models.figure import Figure


class Bishop(Figure):
    picture_white = pygame.image.load('img/bishop.png')
    picture_black = pygame.image.load('img/black_bishop.png')

    def calculate_moves(self):
        possible_moves = [
            self.moves_up_right(),
            self.moves_up_left(),
            self.moves_down_right(),
            self.moves_down_left()
        ]
        return possible_moves

    def __repr__(self):
        return f"Bishop_Object_at_{self.x}/{self.y}"
