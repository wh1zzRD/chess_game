import time

import pygame


class Board:
    """
    Manages all the drawing and GUI in the game.
    """

    def __init__(self, game):
        """
        Args:
            game (Game): game that is being drawn and displayed
        """
        self.game = game

        self.width, self.height = 870, 870
        self.display = pygame.display.set_mode((self.width, self.height))
        self.font = pygame.font.SysFont('Comic Sans MS', 30)

        self.field_side = 100
        self.coordinates_width = 35

        self.brown_color = (97, 53, 7)
        self.beige_color = (218, 163, 120)
        self.green_color = (120, 218, 127)

    def draw(self):
        """
        Runs all draw-methods. This class is only used through this method.
        """
        self.draw_board()
        self.draw_board_coordinates()
        self.draw_selected_figures_moves()
        self.draw_figures()
        pygame.display.flip()

    def draw_board(self):
        """
        Draws the squares of the board.
        """
        self.display.fill(self.brown_color)
        x_field_position = self.coordinates_width
        y_field_position = self.coordinates_width

        for i in range(32):
            pygame.draw.rect(
                self.display,
                self.beige_color,
                pygame.Rect(x_field_position, y_field_position, self.field_side, self.field_side)
            )

            x_field_position += 2 * self.field_side
            if x_field_position == self.width - self.coordinates_width:
                x_field_position = self.coordinates_width + self.field_side
                y_field_position += self.field_side

            elif x_field_position == self.width - self.coordinates_width + self.field_side:
                x_field_position = self.coordinates_width
                y_field_position += self.field_side

    def draw_board_coordinates(self):
        """
        Draws the coordinates on the side of the board.
        """
        y_pos = 65
        x_pos = 75

        # Displaying numbers on left and right side of the field
        for number in range(ord("1"), ord("1") + 8):
            if y_pos == 830:
                y_pos = 30
            letter = self.font.render(chr(number), True, self.beige_color)
            self.display.blit(letter, (845, y_pos))
            self.display.blit(letter, (10, y_pos))
            y_pos += 100

        # Displaying letters on top and bottom of the field
        for symbol in range(ord("A"), ord("A") + 8):
            if x_pos == 840:
                x_pos = 40
            num = self.font.render(chr(symbol), True, self.beige_color)
            self.display.blit(num, (x_pos, 830))
            self.display.blit(num, (x_pos, -5))
            x_pos += 100

    def draw_figures(self):
        """
        Draws the figures of the game.
        """
        for figure in self.game.figures:
            figure.draw()

    def draw_selected_figures_moves(self):
        """
        If there is a selected figure, its moves are displayed on the board.
        """
        if self.game.selected_figure is not None:
            self.game.selected_figure.draw_possible_moves()

    def draw_result(self, result):
        """
        Displays a text on the screen. Used to display result of the game.

        Args:
            result (str): text to be displayed
        """
        result_image = self.font.render("Result: " + str(result), True, self.green_color)
        self.display.blit(result_image, (300, 400))
        pygame.display.update()
        time.sleep(3)

    def convert_mouse_coordinates_to_board_coordinates(self, mouse_coordinates):
        """
        Converts mouse coordinates into the coordinates of the square on the board the mouse is in.
        Args:
            mouse_coordinates (tuple(int, int)): mouse coordinates to be converted

        Returns:
            tuple(int, int): board coordinates
        """
        mouse_x = (mouse_coordinates[0] - self.coordinates_width) // self.field_side
        mouse_y = (mouse_coordinates[1] - self.coordinates_width) // self.field_side

        return mouse_x, mouse_y
