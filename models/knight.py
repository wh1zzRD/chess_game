"""
knight.py
This module provides:
- `Knight(Figure)`: a class to specifically represent a knight in the game.
"""

import os

import pygame

from game.path import get_img_folder_path
from models.figure import Figure


class Knight(Figure):
    """
    This class represents a knight. calculate_moves() is overwritten according to how a knight moves.
    """
    picture_white = pygame.image.load(os.path.join(get_img_folder_path(), "knight.png"))
    picture_black = pygame.image.load(os.path.join(get_img_folder_path(), "black_knight.png"))

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

        return [  # removes moves than are not in (0, 7) range
            [pair for pair in inner_list if all(0 <= num <= 7 for num in pair)]
            for inner_list in possible_moves
        ]

    def __repr__(self):
        return f"Knight_Object_at_{self.x}/{self.y}"
