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
