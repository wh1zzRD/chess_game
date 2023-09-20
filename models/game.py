from typing import Optional

import pygame

from models.chess_util import ChessUtil
from models.fen import FenConverter
from models.figure import Figure
from models.board import Board


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

        self.board = Board(self)

        self.turn = 1
        # self.figures = FenConverter.fen_converter(self, "rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR")
        self.figures = FenConverter.fen_converter(self, "8/8/7k/8/8/8/1K1R4/6R1")

    def run(self):
        while self.keep_doing:
            self.clock.tick(self.FPS)
            self.draw()
            self.process_events()
            self.handle_game_status()

        pygame.quit()

    def draw(self):
        self.board.draw()

    def process_events(self):
        for event in pygame.event.get():
            self.process_exit_event(event)
            self.process_mouse_button_down_event(event)

    def get_figure_in_coords(self, coords):
        for figure in self.figures:
            if figure.x == coords[0] and figure.y == coords[1]:
                return figure
        return None

    def is_mate(self):
        arrangement = ChessUtil(self.figures)
        return arrangement.is_mate(0) or arrangement.is_mate(1)

    def is_check(self):
        arrangement = ChessUtil(self.figures)
        return arrangement.is_check(0) or arrangement.is_check(1)

    def is_stalemate(self):
        arrangement = ChessUtil(self.figures)
        return arrangement.is_stalemate(0) or arrangement.is_stalemate(1)

    def handle_game_status(self):
        if self.is_mate():
            self.keep_doing = False
            self.board.draw()
            self.board.draw_result("checkmate")
        if self.is_stalemate():
            self.keep_doing = False
            self.board.draw()
            self.board.draw_result("stalemate")

    def process_exit_event(self, event):
        if event.type == pygame.QUIT:
            self.keep_doing = False

    def process_mouse_button_down_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:

            mouse_x, mouse_y = self.board.convert_mouse_coordinates_to_board_coordinates(pygame.mouse.get_pos())
            self.figure_selection_events(mouse_x, mouse_y)
            if self.selected_figure is not None:
                self.selected_figure.move(mouse_x, mouse_y)

    def figure_selection_events(self, mouse_x, mouse_y):
        # either selection, deselection or reselection
        if self.selected_figure is None:
            self.handling_figure_selection(mouse_x, mouse_y)
        else:
            self.handling_figure_deselection(mouse_x, mouse_y)

    def handling_figure_deselection(self, mouse_x, mouse_y):
        if mouse_x == self.selected_figure.x and mouse_y == self.selected_figure.y:
            self.selected_figure.deselect()
            self.selected_figure = None

    def handling_figure_selection(self, mouse_x, mouse_y):
        figure = self.get_figure_in_coords((mouse_x, mouse_y))
        if figure is not None and figure.color == self.turn:
            self.selected_figure = figure
            self.selected_figure_moves = figure.get_legal_moves()
            figure.select()

    def handling_figure_post_move(self):
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
