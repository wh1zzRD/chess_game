"""
game_status_handler.py
This module provides:
- `create_new_arrangement(current_arrangement, figure_to_move, move)`: a method to create a new arrangement according
to the move
- `GameStatusHandler`: a class to process legality of moves and arrangements in the game
"""


def create_new_arrangement(current_arrangement, figure_to_move, move):
    """
    Converts the current arrangement of the board into a new one based on the figure being moved and
    the move performed.

    Args:
        current_arrangement (set[Figures]): The current arrangement of the board.
        figure_to_move (Figure): The figure that the player is moving.
        move (tuple): The new coordinates of the figure.

    Returns:
        set[Figures]: The new arrangement of the board.
    """
    new_arrangement = []
    for figure in current_arrangement:
        if figure.x == move[0] and figure.y == move[1] and figure.color != figure_to_move.color:
            continue

        if figure == figure_to_move:
            new_arrangement.append(type(figure)(figure.game, move[0], move[1], figure.color))
        else:
            new_arrangement.append(type(figure)(figure.game, figure.x, figure.y, figure.color))

    return new_arrangement


class GameStatusHandler:
    """
    Handles the aspects regarding the legality of the moves and board arrangements.
    """
    def __init__(self, arrangement):
        """
        Args:
            arrangement (set[Figures]): The current board arrangement.
        """
        self.figures = arrangement.copy()

    def find_king_pos(self, given_side):
        """
        Finds the coordinates of the king of a given color.

        Args:
            given_side (int): The color for which the King's coordinates need to be found.

        Returns:
            tuple(int, int): A list containing the coordinates of the king as two integers.
        """
        for figure in self.figures:
            if figure.is_king and figure.color == given_side:
                return figure.x, figure.y

        raise RuntimeError("There is no king of the given color on the board")

    def find_king(self, given_side):
        """
        Finds the King of a given color.

        Args:
            given_side (int): The color for which the King needs to be found.

        Returns:
            King: The object of the King.
        """
        for figure in self.figures:
            if figure.is_king and figure.color == given_side:
                return figure

        raise RuntimeError("There is no king of the given color on the board")

    def is_any_figure_in_coords(self, coords):
        """
        Checks whether there is any figure in the specific coordinates on the board.

        Args:
            coords (tuple): The coordinates to check.

        Returns:
            Figure or None: The figure if there is any figure in the given coordinates, or None if not.
        """
        for figure in self.figures:
            if figure.x == coords[0] and figure.y == coords[1]:
                return figure
        return None

    def get_moves(self, figure):
        """
        Calculates all legal moves of a figure in the current arrangement.

        Args:
            figure (Figure): The figure whose moves need to be calculated.

        Returns:
            list: A list containing lists of coordinates (int, int) representing all legal moves of the figure.
        """
        possible_moves = figure.calculate_moves()
        legal_moves = []

        for direction in possible_moves:
            for move in direction:
                is_figure_in_way = self.is_any_figure_in_coords(move)
                if is_figure_in_way is not None:
                    if is_figure_in_way.color != figure.color:
                        legal_moves.append(move)
                    break
                legal_moves.append(move)

        return legal_moves

    def is_check(self, given_side):
        """
        Examines whether a given side is now in check.

        Args:
            given_side (int): The color of the side to examine for.

        Returns:
            bool: True if the side is in check, False if not.
        """
        king_pos = self.find_king_pos(given_side)
        for figure in self.figures:
            if figure.color != given_side and king_pos in self.get_moves(figure):
                return True
        return False

    def is_mate(self, given_side):
        """
        Examines whether a given side is now in mate.

        Args:
            given_side (int): The color of the side to examine for.

        Returns:
            bool: True if the side is in mate, False if not.
        """
        if self.is_check(given_side):
            for figure in self.figures:
                if figure.color == given_side:
                    for move in self.get_moves(figure):
                        new_arrangement = GameStatusHandler(create_new_arrangement(self.figures, figure, move))
                        if not new_arrangement.is_check(given_side):
                            return False
            return True
        return False

    def is_stalemate(self, given_side):
        """
        Examines whether a given side is now in stalemate.

        Args:
            given_side (int): The color of the side to examine for.

        Returns:
            bool: True if the side is in stalemate, False if not.
        """
        if not self.is_check(given_side):
            for figure in self.figures:
                if figure.color == given_side:
                    for move in self.get_moves(figure):
                        new_arrangement = GameStatusHandler(create_new_arrangement(self.figures, figure, move))
                        if not new_arrangement.is_check(given_side):
                            return False
            return True
        return False

    def is_move_legal(self, figure, move):
        """
        Checks if the specific move of a figure is legal in the current arrangement.

        Args:
            figure (Figure): The figure that is being moved.
            move (tuple): The new coordinates of the figure.

        Returns:
            bool: True if the move is legal, False if not.
        """
        arrangement_after_move = GameStatusHandler(create_new_arrangement(self.figures, figure, move))
        if not arrangement_after_move.is_check(figure.color):
            return True
        return False

    def is_long_castle_possible(self, given_side):
        if given_side == 1:
            rook = None
            for figure in self.figures:
                if figure.color == given_side and (figure.x, figure.y) == (0, 7) and not figure.been_moved:
                    rook = figure

            if not self.find_king(given_side).been_moved and rook is not None:
                coordinates_between = [(1, 7), (2, 7), (3, 7)]
                no_pieces_between = True
                for coordinates in coordinates_between:
                    if self.is_any_figure_in_coords(coordinates) is not None:
                        no_pieces_between = False

                coordinates_king_passes = [(2, 7), (3, 7), (4, 7)]
                no_checks_between = True
                for coordinates in coordinates_king_passes:
                    temp_figures = create_new_arrangement(self.figures, self.find_king(given_side), coordinates)
                    temp_arrangement = GameStatusHandler(temp_figures)
                    if temp_arrangement.is_check(given_side):
                        no_checks_between = False

                if no_pieces_between and no_checks_between:
                    return True
            return False

        else:
            rook = None
            for figure in self.figures:
                if figure.color == given_side and (figure.x, figure.y) == (0, 0) and not figure.been_moved:
                    rook = figure

            if not self.find_king(given_side).been_moved and rook is not None:
                coordinates_between = [(1, 0), (2, 0), (3, 0)]
                no_pieces_between = True
                for coordinates in coordinates_between:
                    if self.is_any_figure_in_coords(coordinates) is not None:
                        no_pieces_between = False

                coordinates_king_passes = [(2, 0), (3, 0), (4, 0)]
                no_checks_between = True
                for coordinates in coordinates_king_passes:
                    temp_figures = create_new_arrangement(self.figures, self.find_king(given_side), coordinates)
                    temp_arrangement = GameStatusHandler(temp_figures)
                    if temp_arrangement.is_check(given_side):
                        no_checks_between = False

                if no_pieces_between and no_checks_between:
                    return True
            return False

    def is_short_castle_possible(self, given_side):
        if given_side == 1:
            rook = None
            for figure in self.figures:
                if figure.color == given_side and (figure.x, figure.y) == (7, 7) and not figure.been_moved:
                    rook = figure

            if not self.find_king(given_side).been_moved and rook is not None:
                coordinates_between = [(5, 7), (6, 7)]
                no_pieces_between = True
                for coordinates in coordinates_between:
                    if self.is_any_figure_in_coords(coordinates) is not None:
                        no_pieces_between = False

                coordinates_king_passes = [(4, 7), (5, 7), (6, 7)]
                no_checks_between = True
                for coordinates in coordinates_king_passes:
                    temp_figures = create_new_arrangement(self.figures, self.find_king(given_side), coordinates)
                    temp_arrangement = GameStatusHandler(temp_figures)
                    if temp_arrangement.is_check(given_side):
                        no_checks_between = False

                if no_pieces_between and no_checks_between:
                    return True
            return False

        else:
            rook = None
            for figure in self.figures:
                if figure.color == given_side and (figure.x, figure.y) == (7, 0) and not figure.been_moved:
                    rook = figure

            if not self.find_king(given_side).been_moved and rook is not None:
                coordinates_between = [(5, 0), (6, 0)]
                no_pieces_between = True
                for coordinates in coordinates_between:
                    if self.is_any_figure_in_coords(coordinates) is not None:
                        no_pieces_between = False

                coordinates_king_passes = [(4, 0), (5, 0), (6, 0)]
                no_checks_between = True
                for coordinates in coordinates_king_passes:
                    temp_figures = create_new_arrangement(self.figures, self.find_king(given_side), coordinates)
                    temp_arrangement = GameStatusHandler(temp_figures)
                    if temp_arrangement.is_check(given_side):
                        no_checks_between = False

                if no_pieces_between and no_checks_between:
                    return True
            return False
