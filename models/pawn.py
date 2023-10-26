"""
pawn.py
This module provides:
- `Pawn(Figure)`: a class to specifically represent a pawn in the game.
"""

import os

import pygame

from game.path import get_img_folder_path
from game.utils.game_status_handler import GameStatusHandler
from models.figure import Figure
from models.queen import Queen


class Pawn(Figure):
    """
    This class represents a pawn. calculate_moves() is overwritten according to how a pawn moves.
    """
    picture_white = pygame.image.load(os.path.join(get_img_folder_path(), "pawn.png"))
    picture_black = pygame.image.load(os.path.join(get_img_folder_path(), "black_pawn.png"))

    def calculate_moves(self):
        return self.basic_move() + self.diagonal_take()

    def diagonal_take(self):
        """
        If there is a piece of the opposing color diagonally from a pawn that this move is added to
        possible moves.

        Returns:
            list[list[tuple(int, int)]]: possible moves diagonally
        """
        arrangement = GameStatusHandler(self.game.figures)
        extra_moves = []

        if self.color == 1:
            possible_figure1 = arrangement.is_any_figure_in_coords((self.x - 1, self.y - 1))
            possible_figure2 = arrangement.is_any_figure_in_coords((self.x + 1, self.y - 1))

            if possible_figure1 is not None and possible_figure1.color == 0:
                extra_moves.append([(self.x - 1, self.y - 1)])
            if possible_figure2 is not None and possible_figure2.color == 0:
                extra_moves.append([(self.x + 1, self.y - 1)])
        else:
            possible_figure1 = arrangement.is_any_figure_in_coords((self.x - 1, self.y + 1))
            possible_figure2 = arrangement.is_any_figure_in_coords((self.x + 1, self.y + 1))

            if possible_figure1 is not None and possible_figure1.color == 1:
                extra_moves.append([(self.x - 1, self.y + 1)])
            if possible_figure2 is not None and possible_figure2.color == 1:
                extra_moves.append([(self.x + 1, self.y + 1)])

        return extra_moves

    def basic_move(self):
        """
        Calculates the basic moves of a pawn. Either just one square, or if the pawn is on the starting rank
        also two squares to the front.

        Returns:
            list[list[tuple(int, int)]]: possible moves forward
        """
        moves = []
        arrangement = GameStatusHandler(self.game.figures)

        if self.color == 1:
            if arrangement.is_any_figure_in_coords((self.x, self.y - 1)) is None:
                moves.append([(self.x, self.y - 1)])
                if self.y == 6 and arrangement.is_any_figure_in_coords((self.x, self.y - 2)) is None:
                    moves.append([(self.x, self.y - 2)])
        else:
            if arrangement.is_any_figure_in_coords((self.x, self.y + 1)) is None:
                moves.append([(self.x, self.y + 1)])
                if self.y == 1 and arrangement.is_any_figure_in_coords((self.x, self.y + 2)) is None:
                    moves.append([(self.x, self.y + 2)])

        return moves

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
