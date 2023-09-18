import pygame

from models.figure import Figure


class Knight(Figure):
    picture_white = pygame.image.load('img/knight.png')
    picture_black = pygame.image.load('img/black_knight.png')

    def calculate_moves(self):
        possible_moves = [
            [(self.x - 1, self.y - 2)],
            [(self.x + 1, self.y - 2)],
            [(self.x + 2, self.y - 1)],
            [(self.x + 2, self.y + 1)],
            [(self.x + 1, self.y + 2)],
            [(self.x - 1, self.y + 2)],
            [(self.x - 2, self.y + 1)],
            [(self.x - 2, self.y - 1)],
        ]
        return possible_moves

    def __repr__(self):
        return f"Knight_Object_at_{self.x}/{self.y}"
