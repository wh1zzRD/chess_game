"""
bishop.py
This module provides:
- `Bishop(Figure)`: a class to specifically represent a bishop in the game.
"""

import os

import pygame

from models.figure import Figure
from game.path import get_img_folder_path


class Bishop(Figure):
    """
    This class represents a bishop. calculate_moves() is overwritten according to how a bishop moves.
    """
    picture_white = pygame.image.load(os.path.join(get_img_folder_path(), "bishop.png"))
    picture_black = pygame.image.load(os.path.join(get_img_folder_path(), "black_bishop.png"))

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
