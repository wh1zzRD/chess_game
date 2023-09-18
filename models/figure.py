from typing import Optional

import pygame


# from models.king import King
# from models.pawn import Pawn


class Figure:

    @property
    def picture_white(self):
        raise NotImplementedError()

    @property
    def picture_black(self):
        raise NotImplementedError()

    # When creating a figure: passing game object, position on the board and color.
    # Figure gets an image assigned from its own class
    def __init__(self, game, x, y, color):  # TODO change parameters x, y to tuple
        self.game = game
        self.x = x
        self.y = y
        self.color = color  # 1 white  0 black
        self.is_selected = False
        if color:
            self.image = pygame.transform.rotozoom(self.picture_white, 0, 0.4)
            self.factor = 1
        else:
            self.image = pygame.transform.rotozoom(self.picture_black, 0, 0.4)
            self.factor = -1

    def __repr__(self):
        raise NotImplementedError

    def draw(self):
        self.game.display.blit(self.image, (self.x * 100 + 35, self.y * 100 + 35))

    def set_as_selected(self):
        if self.is_selected:
            return
        self.is_selected = True
        self.image = pygame.transform.rotozoom(self.image, 0, 1.1)

    def deselect(self):
        self.is_selected = False
        if self.color:
            self.image = pygame.transform.rotozoom(self.picture_white, 0, 0.4)
        else:
            self.image = pygame.transform.rotozoom(self.picture_black, 0, 0.4)

    def move(self, mouse_x, mouse_y):  # TODO change mouse coordinates to a tuple

        mouse_coordinates = (mouse_x, mouse_y)  # Coordinates of a field, where user  tries to move the figure
        figure_to_delete: Optional[Figure] = None

        if mouse_coordinates in self.remove_if_check():  # If the field is a possible move for this figure
            figure_in_coords = self.is_any_figure_in_coords(mouse_coordinates)
            if figure_in_coords:
                for figure in self.game.figures:
                    if figure == figure_in_coords:
                        self.game.figures.remove(figure_in_coords)
                        break
            self.x, self.y = mouse_coordinates
            return True
        else:
            return False

    def display_possible_moves(self, moves):
        # Displaying a circle on every field on the board that is a possible move for the figure
        for move in moves:
            pygame.draw.circle(self.game.display, (80, 80, 80), (move[0] * 100 + 85, move[1] * 100 + 85), 20)

        # Drawing figures once more, so they are over the circles for moves
        for figure in self.game.figures:
            figure.draw()

    def calculate_moves(self):
        raise NotImplementedError("This method should be implemented in child classes")

    def is_any_figure_in_coords(self, coords):
        # TODO move to Game
        for figure in self.game.calculation_figures:
            if figure.x == coords[0] and figure.y == coords[1]:
                return figure
        return False

    def remove_if_figure(self):
        possible_moves = self.calculate_moves()
        legal_moves = []

        for direction in possible_moves:
            for move in direction:
                is_figure_in_way = self.is_any_figure_in_coords(move)
                if is_figure_in_way:
                    if is_figure_in_way.color != self.color:
                        legal_moves.append(move)
                    break
                legal_moves.append(move)

        return legal_moves

    def remove_if_check(self):
        """
        If a move in possible moves will lead to a check after your move, respectively to checkmate for you on
        opponent's move, such move is removed from possible moves
        """
        possible_moves = self.remove_if_figure()
        legal_moves = []
        for move in possible_moves:
            new_arrangement = self.game.create_temp_arrangement(self, move)
            if not self.game.is_check_in_given_arrangement(new_arrangement, self.color):
                legal_moves.append(move)

        return legal_moves

    def moves_right(self):
        """
        Calculates the possible moves of the figure from current position to the right end of the board (horizontally)
        (ignoring the pieces)
        :return: possible moves
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
        (ignoring the pieces)
        :return: possible moves
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
        (ignoring the pieces)
        :return: possible moves
        :return:
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
        (ignoring the pieces)
        :return: possible moves
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
        (ignoring the pieces)
        :return: possible moves
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
        (ignoring the pieces)
        :return: possible moves
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
        (ignoring the pieces)
        :return: possible moves
        :return:
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
        (ignoring the pieces)
        :return: possible moves
        """
        possible_moves = []
        temp_x, temp_y = self.x - 1, self.y + 1
        while temp_x >= 0 and temp_y <= 7:
            possible_moves.append((temp_x, temp_y))
            temp_x -= 1
            temp_y += 1

        return possible_moves
