"""
queen.py
This module provides:
- `Bishop(Figure)`: a class to specifically represent a queen in the game.
"""

import os

import pygame

from game.path import get_img_folder_path
from models.figure import Figure


class Queen(Figure):
    """
    This class represents a queen. calculate_moves() is overwritten according to how a queen moves.
    """
    picture_white = pygame.image.load(os.path.join(get_img_folder_path(), "queen.png"))
    picture_black = pygame.image.load(os.path.join(get_img_folder_path(), "black_queen.png"))

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
