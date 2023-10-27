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
        return self.basic_move() + self.diagonal_take() + self.calculate_en_passant()

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

    def calculate_en_passant(self):
        """
        Calculates whether there is a possibility for en passant for this pawn right now.

        Returns:
            list[list[tuple(int, int)]]: en passant moves to take other pawns
        """
        en_passant_moves = []
        if self.game.en_passant is not None:
            if self.color == 1:
                if self.game.en_passant.x in [self.x - 1, self.x + 1] and self.game.en_passant.y == self.y:
                    en_passant_moves.append([(self.game.en_passant.x, self.game.en_passant.y - 1)])
            else:
                if self.game.en_passant.x in [self.x - 1, self.x + 1] and self.game.en_passant.y == self.y:
                    en_passant_moves.append([(self.game.en_passant.x, self.game.en_passant.y + 1)])
        return en_passant_moves

    def __repr__(self):
        return f"Pawn_Object_at_{self.x}/{self.y}"

    def move(self, mouse_x, mouse_y):
        prev_x, prev_y = self.x, self.y
        super().move(mouse_x, mouse_y)
        self.remove_figure_after_en_passant(prev_x, prev_y)
        self.set_en_passant(prev_y)
        # Turning Pawn into Queen if it's on the end of the board
        if isinstance(self, Pawn) and ((self.y == 0 and self.color == 1) or (self.y == 7 and self.color == 0)):
            self.pawn_to_queen()
            self.game.pawn_switched_to_queen = True

    def set_en_passant(self, prev_y):
        """
        If the pawn has been moved two squares to the front, the en passant flag of the game is set.

        Args:
            prev_y (int): previous y position of this pawn
        """
        if abs(prev_y - self.y) == 2:
            self.game.en_passant = self

    def remove_figure_after_en_passant(self, prev_x, prev_y):
        """
        If this pawn has been moved in the en passant shape (1 forward and 1 to the side) a piece has to be removed
        since en passant always is a take.

        Args:
            prev_x (int): previous x position of this pawn
            prev_y (int): previous y position of this pawn
        """
        if abs(prev_x - self.x) == 1 and abs(prev_y - self.y) == 1:
            figure_in_coords = self.game.get_figure_in_coords((self.x, prev_y))
            if figure_in_coords:
                for figure in self.game.figures:
                    if figure == figure_in_coords:
                        self.game.figures.remove(figure_in_coords)
                        break

    def pawn_to_queen(self):
        """
        Replaces the object of the pawn with the object of a Queen in the same coordinates.
        """
        self.game.figures.add(Queen(self.game, self.x, self.y, self.color))
        self.game.figures.remove(self)
