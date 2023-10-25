import os

import pygame

from models.figure import Figure
from game.Path import get_img_folder_path


class Bishop(Figure):
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
