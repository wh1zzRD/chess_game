import os

import pygame

from game.Path import get_img_folder_path
from models.figure import Figure


class King(Figure):
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

        # TODO add the same check to Knight class
        return [  # removes moves than are not in (0, 7) range
            [pair for pair in inner_list if all(0 <= num <= 7 for num in pair)]
            for inner_list in possible_moves
        ]

    def __repr__(self):
        return f"King Object at {self.x} {self.y}"
