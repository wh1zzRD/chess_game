"""
figure.py
This module provides:
- `Figure`: a parent class for all the pieces in the game.
"""

import pygame

from game.utils.game_status_handler import GameStatusHandler


class Figure:
    """
    Class that describes a generic piece. The attributes are coordinates, color and the game.
    """

    @property
    def picture_white(self):
        """
        Get the picture of the white figure associated with this object.

        This property is intended to be implemented in subclasses.
        Subclasses should provide the black picture by loading it from img folder.

        Raises:
            NotImplementedError: This property is not implemented in the base class.
        """
        raise NotImplementedError()

    @property
    def picture_black(self):
        """
        Get the picture of the black figure associated with this object.

        This property is intended to be implemented in subclasses.
        Subclasses should provide the black picture by loading it from img folder.

        Raises:
            NotImplementedError: This property is not implemented in the base class.
        """
        raise NotImplementedError()

    @property
    def is_king(self):
        """
        Whether the figure is a King or not. This method should be overwritten in class King.
        Returns:
            bool: True if that is the case, False if not
        """
        return False

    def __init__(self, game, x, y, color):
        """
        Args:
            game (Game): game object
            x (int): x coordinate of the figure
            y (int): y coordinate of the figure
            color (int): side / color of the figure
        """
        self.game = game
        self.x = x
        self.y = y
        self.color = color  # 1 white  0 black
        self.is_selected = False
        self.been_moved = False
        if color:
            self.image = pygame.transform.rotozoom(self.picture_white, 0, 1.6)
            self.factor = 1
        else:
            self.image = pygame.transform.rotozoom(self.picture_black, 0, 1.6)
            self.factor = -1

    def __repr__(self):
        raise NotImplementedError

    def draw(self):
        """Draws the figure on the screen in its coordinates."""
        self.game.board.display.blit(self.image, (self.x * 100 + 35, self.y * 100 + 35))

    def select(self):
        """Makes the image of the figure bigger, when it's selected."""
        if self.is_selected:
            return
        self.is_selected = True
        self.image = pygame.transform.rotozoom(self.image, 0, 1.1)

    def deselect(self):
        """Makes the image of the figure normal, when it's deselected."""
        self.is_selected = False
        if self.color:
            self.image = pygame.transform.rotozoom(self.picture_white, 0, 1.6)
        else:
            self.image = pygame.transform.rotozoom(self.picture_black, 0, 1.6)

    def move(self, mouse_x, mouse_y):
        """
        Moves the figure to the given coordinates if it is possible.

        Args:
            mouse_x (int): x coordinate of the field, where the player tries to move the figure
            mouse_y (int): y coordinate of the field, where the player tries to move the figure

        Returns:
            bool: True if move was possible (legal) and the figure was moved and False is not
        """
        mouse_coordinates = (mouse_x, mouse_y)
        if mouse_coordinates in self.get_legal_moves():
            figure_in_coords = self.game.get_figure_in_coords(mouse_coordinates)
            if figure_in_coords:
                for figure in self.game.figures:
                    if figure == figure_in_coords:
                        self.game.figures.remove(figure_in_coords)
                        break
            self.x, self.y = mouse_coordinates
            if not self.been_moved:
                self.been_moved = True

            self.game.turn = not self.color
            self.deselect()
            self.game.selected_figure = None

            self.game.en_passant = None

    def draw_possible_moves(self):
        """Draws the possible moves of the figure as circles in the respective coordinates."""
        for move in self.get_legal_moves():
            pygame.draw.circle(self.game.board.display, (80, 80, 80), (move[0] * 100 + 85, move[1] * 100 + 85), 20)

    def calculate_moves(self):
        """
        Calculates all possible moves of the figure, ignoring its legality and other figures. Only considers the
        edges of the board or specific rules on how the figure can move (e.g. King, Pawn, knight).
        This method should be overwritten for each subclass of Figure, since all figures move differently.

        Returns:
            list[tuple(int, int)]: possible moves
        """
        raise NotImplementedError("This method should be implemented in child classes")

    def get_all_moves(self):
        """
        If the path to the move is blocked by a different figure, that move and all the next moves on the same path
        are removed from possible moves. If the figure blocking the path is the figure of the opposing color, that move
        is still added to the possible moves (representing capturing the figure), but all the following ones are not.

        Returns:
            list[tuple(int, int)]: moves that are not blocked by other figures
        """
        possible_moves = self.calculate_moves()
        legal_moves = []

        for direction in possible_moves:
            for move in direction:
                is_figure_in_way = self.game.get_figure_in_coords(move)
                if is_figure_in_way:
                    if is_figure_in_way.color != self.color:
                        legal_moves.append(move)
                    break
                legal_moves.append(move)

        return legal_moves

    def get_legal_moves(self):
        """
        If the move is not legal, or rather will put you in check, such move is not added to legal moves.
        Also add castling moves to the possible moves if self is the king and castling is possible.

        Returns:
            list[tuple(int, int)]: list with legal moves
        """
        possible_moves = self.get_all_moves()
        legal_moves = []
        for move in possible_moves:
            current_arrangement = GameStatusHandler(self.game.figures)
            if current_arrangement.is_move_legal(self, move):
                legal_moves.append(move)

        if self.is_king:
            arrangement = GameStatusHandler(self.game.figures)

            if arrangement.is_short_castle_possible(self.color):
                if self.color == 1:
                    legal_moves.append((6, 7))
                else:
                    legal_moves.append((6, 0))
            if arrangement.is_long_castle_possible(self.color):
                if self.color == 1:
                    legal_moves.append((2, 7))
                else:
                    legal_moves.append((2, 0))

        return legal_moves

    def moves_right(self):
        """
        Calculates the possible moves of the figure from current position to the right end of the board (horizontally)
        (ignoring the pieces). Only considers the edges of the board.

        Returns:
            list[tuple(int, int)]: possible moves
        """
        possible_moves = []
        temp_x = self.x + 1
        while temp_x <= 7:
            possible_moves.append((temp_x, self.y))
            temp_x += 1

        return possible_moves

    def moves_left(self):
        """
        Calculates the possible moves of the figure from current position to the left end of the board (horizontally)
        (ignoring the pieces). Only considers the edges of the board.

        Returns:
            list[tuple(int, int)]: possible moves
        """
        possible_moves = []
        temp_x = self.x - 1
        while temp_x >= 0:
            possible_moves.append((temp_x, self.y))
            temp_x -= 1

        return possible_moves

    def moves_up(self):
        """
        Calculates the possible moves of the figure from current position to the top end of the board (vertically)
        (ignoring the pieces). Only considers the edges of the board.

        Returns:
            list[tuple(int, int)]: possible moves
        """
        possible_moves = []
        temp_y = self.y - 1
        while temp_y >= 0:
            possible_moves.append((self.x, temp_y))
            temp_y -= 1

        return possible_moves

    def moves_down(self):
        """
        Calculates the possible moves of the figure from current position to the bottom end of the board (vertically)
        (ignoring the pieces). Only considers the edges of the board.

        Returns:
            list[tuple(int, int)]: possible moves
        """
        possible_moves = []
        temp_y = self.y + 1
        while temp_y <= 7:
            possible_moves.append((self.x, temp_y))
            temp_y += 1

        return possible_moves

    def moves_up_right(self):
        """
        Calculates the possible moves of the figure from current position going up and right (diagonally)
        (ignoring the pieces). Only considers the edges of the board.

        Returns:
            list[tuple(int, int)]: possible moves
        """
        possible_moves = []
        temp_x, temp_y = self.x + 1, self.y - 1
        while temp_x <= 7 and temp_y >= 0:
            possible_moves.append((temp_x, temp_y))
            temp_x += 1
            temp_y -= 1

        return possible_moves

    def moves_up_left(self):
        """
        Calculates the possible moves of the figure from current position going up and left (diagonally)
        (ignoring the pieces). Only considers the edges of the board.

        Returns:
            list[tuple(int, int)]: possible moves
        """
        possible_moves = []
        temp_x, temp_y = self.x - 1, self.y - 1
        while temp_x >= 0 and temp_y >= 0:
            possible_moves.append((temp_x, temp_y))
            temp_x -= 1
            temp_y -= 1

        return possible_moves

    def moves_down_right(self):
        """
        Calculates the possible moves of the figure from current position going down and right (diagonally)
        (ignoring the pieces). Only considers the edges of the board.

        Returns:
            list[tuple(int, int)]: possible moves
        """
        possible_moves = []
        temp_x, temp_y = self.x + 1, self.y + 1
        while temp_x <= 7 and temp_y <= 7:
            possible_moves.append((temp_x, temp_y))
            temp_x += 1
            temp_y += 1

        return possible_moves

    def moves_down_left(self):
        """
        Calculates the possible moves of the figure from current position going down and left (diagonally)
        (ignoring the pieces). Only considers the edges of the board.

        Returns:
            list[tuple(int, int)]: possible moves
        """
        possible_moves = []
        temp_x, temp_y = self.x - 1, self.y + 1
        while temp_x >= 0 and temp_y <= 7:
            possible_moves.append((temp_x, temp_y))
            temp_x -= 1
            temp_y += 1

        return possible_moves
