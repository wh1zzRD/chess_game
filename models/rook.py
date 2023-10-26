"""
rook.py
This module provides:
- `Rook(Figure)`: a class to specifically represent a rook in the game.
"""

import os

import pygame

from game.path import get_img_folder_path
from models.figure import Figure


class Rook(Figure):
    """
    This class represents a rook. calculate_moves() is overwritten according to how a rook moves.
    """
    picture_white = pygame.image.load(os.path.join(get_img_folder_path(), "rook.png"))
    picture_black = pygame.image.load(os.path.join(get_img_folder_path(), "black_rook.png"))

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
