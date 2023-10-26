"""
pawn.py
This module provides:
- `Pawn(Figure)`: a class to specifically represent a pawn in the game.
"""

import os

import pygame

from game.path import get_img_folder_path
from models.figure import Figure
from models.queen import Queen


class Pawn(Figure):
    """
    This class represents a pawn. calculate_moves() is overwritten according to how a pawn moves.
    """
    picture_white = pygame.image.load(os.path.join(get_img_folder_path(), "pawn.png"))
    picture_black = pygame.image.load(os.path.join(get_img_folder_path(), "black_pawn.png"))

    def calculate_moves(self):
        if self.color:
            possible_moves = [[(self.x, self.y - 1)]]
        else:
            possible_moves = [[(self.x, self.y + 1)]]

        return possible_moves

    def __repr__(self):
        return f"Pawn_Object_at_{self.x}/{self.y}"

    def move(self, mouse_x, mouse_y):
        super().move(mouse_x, mouse_y)
        # Turning Pawn into Queen if it's on the end of the board
        if isinstance(self, Pawn) and ((self.y == 0 and self.color == 1) or (self.y == 7 and self.color == 0)):
            self.pawn_to_queen()
            self.game.pawn_switched_to_queen = True

    def pawn_to_queen(self):
        """
        Replaces the object of the pawn with the object of a Queen in the same coordinates.
        """
        self.game.figures.add(Queen(self.game, self.x, self.y, self.color))
        self.game.figures.remove(self)
