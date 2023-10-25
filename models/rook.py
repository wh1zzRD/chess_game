import os

import pygame

from game.Path import get_img_folder_path
from models.figure import Figure


class Rook(Figure):
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
