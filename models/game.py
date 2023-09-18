import time
from typing import Optional

import pygame

from models.fen import FenConverter
from models.figure import Figure
from models.bishop import Bishop
from models.king import King
from models.knight import Knight
from models.pawn import Pawn
from models.queen import Queen
from models.rook import Rook


class Game:

    def __init__(self):
        pygame.init()
        width, height = 870, 870
        self.FPS = 40
        self.display = pygame.display.set_mode((width, height))
        self.clock = pygame.time.Clock()
        self.font = pygame.font.SysFont('Comic Sans MS', 30)

        self.pawn_switched_to_queen = False

        self.selected_figure: Optional[Figure] = None
        self.selected_figure_moves = []
        self.keep_doing = True

        self.check = False
        self.mate = False
        self.stalemate = False
        self.result = None
        self.turn = 1
        # self.figures = FenConverter.fen_converter(self, "rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR")
        self.figures = FenConverter.fen_converter(self, "2rr4/8/6k1/8/8/2Q5/2K5/8")
        # self.figures = FenConverter.fen_converter(self, "2r5/3r4/6k1/8/8/8/1K6/8")
        self.calculation_figures = self.figures.copy()

    def display_field(self):
        self.display.fill((97, 53, 7))
        x_field_position = 35
        y_field_position = 35

        for i in range(32):
            # color = (97, 53, 7)
            color = (218, 163, 120)
            pygame.draw.rect(self.display, color, pygame.Rect(x_field_position, y_field_position, 100, 100))

            x_field_position += 200
            if x_field_position == 835:
                x_field_position = 135
                y_field_position += 100

            elif x_field_position == 935:
                x_field_position = 35
                y_field_position += 100

    def display_coordinates(self):
        y_pos = 65
        x_pos = 75

        # Displaying numbers on left and right side of the field
        for number in range(ord("1"), ord("1") + 8):
            if y_pos == 830:
                y_pos = 30
            letter = self.font.render(chr(number), True, (218, 163, 120))
            self.display.blit(letter, (845, y_pos))
            self.display.blit(letter, (10, y_pos))
            y_pos += 100

        # Displaying letters on top and bottom of the field
        for symbol in range(ord("A"), ord("A") + 8):
            if x_pos == 840:
                x_pos = 40
            num = self.font.render(chr(symbol), True, (218, 163, 120))
            self.display.blit(num, (x_pos, 830))
            self.display.blit(num, (x_pos, -5))
            x_pos += 100

    def display_figures(self):
        for figure in self.figures:
            figure.draw()

    def display_result(self):
        if self.mate or self.stalemate:
            result_image = self.font.render("Result: " + str(self.result), True, (120, 218, 127))
            self.display.blit(result_image, (300, 400))
            pygame.display.update()
            time.sleep(3)
            self.keep_doing = False

    def display_selected_figures_moves(self):
        if self.selected_figure is not None:
            self.selected_figure.display_possible_moves(self.selected_figure_moves)

    def check_mate(self):
        for figure in self.figures:
            if figure.color != self.turn:
                if figure.remove_if_check():
                    self.mate = False
                    return False

        self.mate = True
        return True

    def check_check(self):
        king_pos = None
        for figure in self.figures:
            if isinstance(figure, King) and figure.color != self.turn:
                king_pos = [figure.x, figure.y]
                break

        for figure in self.figures:
            if figure.color == self.turn:
                if king_pos in figure.calculate_moves():
                    self.check = True
                    return True

        self.check = False
        return False

    def handle_game_status(self):
        if self.check_check() and self.check_mate():
            self.result = "checkmate"
        if not self.check_check() and self.check_mate():
            self.mate = False
            self.stalemate = True
            self.result = "stalemate"

    @staticmethod
    def convert_mouse_coordinates_to_field_coordinates(mouse_coordinates):
        mouse_x = (mouse_coordinates[0] - 35) // 100
        mouse_y = (mouse_coordinates[1] - 35) // 100

        return mouse_x, mouse_y

    def process_exit_event(self, event):
        if event.type == pygame.QUIT:
            self.keep_doing = False

    def process_figure_handling_event(self, event):
        self.calculation_figures = self.figures.copy()
        if event.type == pygame.MOUSEBUTTONDOWN:

            if event.button == 1:
                mouse_x, mouse_y = self.convert_mouse_coordinates_to_field_coordinates(pygame.mouse.get_pos())

                if self.selected_figure is not None:
                    if self._handling_figure_deselection(mouse_x, mouse_y):
                        return
                    if self.selected_figure.move(mouse_x, mouse_y):
                        self._handling_figure_post_move()
                else:
                    self._handling_figure_selection(mouse_x, mouse_y)

    def _handling_figure_deselection(self, mouse_x, mouse_y):
        if mouse_x == self.selected_figure.x and mouse_y == self.selected_figure.y:
            self.selected_figure.deselect()
            self.selected_figure = None
            return True

        return False

    def _handling_figure_post_move(self):
        if self.pawn_switched_to_queen:
            for figure in self.figures:
                if [figure.x, figure.y] == [self.selected_figure.x, self.selected_figure.y]:
                    self.selected_figure = figure
                    self.pawn_switched_to_queen = False
                    break

        self.handle_game_status()

        self.turn = not self.selected_figure.color
        self.selected_figure.deselect()
        self.selected_figure = None

    def _handling_figure_selection(self, mouse_x, mouse_y):
        for figure in self.figures:
            if mouse_x == figure.x and mouse_y == figure.y:
                if figure.color == self.turn:
                    figure.set_as_selected()
                    self.selected_figure_moves = figure.remove_if_check()
                    print(self.selected_figure_moves)
                    self.selected_figure = figure
                    break

    def is_check_in_given_arrangement(self, arrangement, given_side_color):
        king_pos = ()
        for figure in arrangement:
            if isinstance(figure, King) and figure.color == given_side_color:
                king_pos = (figure.x, figure.y)
                # TODO add break when found

        for figure in arrangement:
            if figure.color != given_side_color and king_pos in figure.remove_if_figure():
                return True

        return False

    def create_temp_arrangement(self, given_figure, new_pos):
        self.calculation_figures = []
        for figure in self.figures:
            if figure == given_figure:
                self.calculation_figures.append(type(figure)(self, new_pos[0], new_pos[1], figure.color))
            else:
                self.calculation_figures.append(figure)

        return self.calculation_figures
