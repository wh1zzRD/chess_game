import unittest

from models.chess_util import ChessUtil
from models.fen import FenConverter
from models.game import Game

from models.pawn import Pawn
from models.king import King
from models.bishop import Bishop
from models.queen import Queen
from models.knight import Knight
from models.rook import Rook


def get_figure(figures, figure_type, x, y):
    for figure in figures:
        if isinstance(figure, figure_type) and figure.x == x and figure.y == y:
            return figure


class LegalMoveTest(unittest.TestCase):
    def test_one(self):
        game = Game()
        arrangement = FenConverter.fen_converter(game, "rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR")
        f = get_figure(arrangement, Pawn, 2, 6)
        util = ChessUtil(arrangement)
        self.assertEqual(util.is_move_legal(f, (2, 5)), True)

    def test_two(self):
        game = Game()
        arrangement = FenConverter.fen_converter(game, "2r5/8/8/7k/8/2Q5/2K5/8")
        f = get_figure(arrangement, Queen, 2, 5)
        util = ChessUtil(arrangement)
        self.assertEqual(util.is_move_legal(f, (3, 5)), False)

    def test_three(self):
        game = Game()
        arrangement = FenConverter.fen_converter(game, "2r5/8/8/7k/8/2Q5/2K5/8")
        f = get_figure(arrangement, Queen, 2, 5)
        util = ChessUtil(arrangement)
        self.assertEqual(util.is_move_legal(f, (2, 0)), True)

    def test_four(self):
        game = Game()
        arrangement = FenConverter.fen_converter(game, "2Q5/8/8/7k/8/8/2K5/8")
        f = get_figure(arrangement, King, 2, 6)
        util = ChessUtil(arrangement)
        self.assertEqual(util.is_move_legal(f, (1, 6)), True)

    def test_five(self):
        game = Game()
        arrangement = FenConverter.fen_converter(game, "2Q5/7k/8/8/8/8/2K5/8")
        f = get_figure(arrangement, King, 7, 1)
        util = ChessUtil(arrangement)
        self.assertEqual(util.is_move_legal(f, (7, 0)), False)

    def test_six(self):
        game = Game()
        arrangement = FenConverter.fen_converter(game, "8/7k/6b1/8/4Q3/8/2K5/8")
        f = get_figure(arrangement, Bishop, 6, 2)
        util = ChessUtil(arrangement)
        self.assertEqual(util.is_move_legal(f, (4, 4)), True)

    def test_seven(self):
        game = Game()
        arrangement = FenConverter.fen_converter(game, "8/7k/8/8/2KN3r/8/8/7R")
        f = get_figure(arrangement, Knight, 3, 4)
        util = ChessUtil(arrangement)
        self.assertEqual(util.is_move_legal(f, (2, 2)), False)

    def test_eight(self):
        game = Game()
        arrangement = FenConverter.fen_converter(game, "8/7k/8/8/2KN3r/8/8/7R")
        f = get_figure(arrangement, Rook, 7, 4)
        util = ChessUtil(arrangement)
        self.assertEqual(util.is_move_legal(f, (3, 4)), False)

    def test_nine(self):
        game = Game()
        arrangement = FenConverter.fen_converter(game, "8/7k/8/8/2KN3r/8/8/7R")
        f = get_figure(arrangement, Rook, 7, 7)
        util = ChessUtil(arrangement)
        self.assertEqual(util.is_move_legal(f, (7, 4)), True)

    def test_ten(self):
        game = Game()
        arrangement = FenConverter.fen_converter(game, "8/7k/8/8/2K5/8/8/6R1")
        f = get_figure(arrangement, King, 7, 1)
        util = ChessUtil(arrangement)
        self.assertEqual(util.is_move_legal(f, (6, 1)), False)
