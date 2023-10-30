"""
king.py
This module provides:
- `King(Figure)`: a class to specifically represent a king in the game.
"""

import os

import pygame

from game.path import get_img_folder_path
from game.utils.game_status_handler import GameStatusHandler
from models.figure import Figure


class King(Figure):
    """
    This class represents a king. calculate_moves() is overwritten according to how a king moves.
    """
    picture_white = pygame.image.load(os.path.join(get_img_folder_path(), "king.png"))
    picture_black = pygame.image.load(os.path.join(get_img_folder_path(), "black_king.png"))

    @property
    def is_king(self):
        """
        This figure is a King
        Returns:
            bool: True since this figure is the King
        """
        return True

    def calculate_moves(self):
        possible_moves = [
            [(self.x - 1, self.y - 1)],
            [(self.x, self.y - 1)],
            [(self.x + 1, self.y - 1)],
            [(self.x + 1, self.y)],
            [(self.x + 1, self.y + 1)],
            [(self.x, self.y + 1)],
            [(self.x - 1, self.y + 1)],
            [(self.x - 1, self.y)],
        ]

        return [  # removes moves than are not in (0, 7) range
            [pair for pair in inner_list if all(0 <= num <= 7 for num in pair)]
            for inner_list in possible_moves
        ]

    def move(self, mouse_x, mouse_y):
        prev_x, prev_y = self.x, self.y
        super().move(mouse_x, mouse_y)
        self.handle_post_castle_situation(prev_x, prev_y)

    def handle_post_castle_situation(self, prev_x, prev_y):
        arrangement = GameStatusHandler(self.game.figures)
        if abs(self.x - prev_x) == 2:
            if self.color == 1:
                if self.x == 2:
                    rook = arrangement.is_any_figure_in_coords((0, 7))
                    rook.x = 3
                elif self.x == 6:
                    rook = arrangement.is_any_figure_in_coords((7, 7))
                    rook.x = 5
            else:
                if self.x == 2:
                    rook = arrangement.is_any_figure_in_coords((0, 0))
                    rook.x = 3
                elif self.x == 6:
                    rook = arrangement.is_any_figure_in_coords((7, 0))
                    rook.x = 5

    def __repr__(self):
        return f"King Object at {self.x} {self.y}"
