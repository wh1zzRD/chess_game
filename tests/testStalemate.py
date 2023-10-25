import unittest

from game.utils.game_status_handler import GameStatusHandler
from game.utils.fen import FenConverter
from game.game import Game


class StalemateTest(unittest.TestCase):

    def test_one(self):
        game = Game()
        arrangement = FenConverter.fen_converter(game, "1r6/8/8/7k/8/8/7r/K7")
        util = GameStatusHandler(arrangement)
        self.assertEqual(util.is_stalemate(1), True)

    def test_two(self):
        game = Game()
        arrangement = FenConverter.fen_converter(game, "1r6/8/8/7k/8/7r/8/K7")
        util = GameStatusHandler(arrangement)
        self.assertEqual(util.is_stalemate(1), False)

    def test_three(self):
        game = Game()
        arrangement = FenConverter.fen_converter(game, "1r6/8/8/7k/8/7r/8/K7")
        util = GameStatusHandler(arrangement)
        self.assertEqual(util.is_stalemate(0), False)

    def test_four(self):
        game = Game()
        arrangement = FenConverter.fen_converter(game, "R4B2/8/n7/7K/k2N4/8/8/4Q3")
        util = GameStatusHandler(arrangement)
        self.assertEqual(util.is_stalemate(0), True)

    def test_five(self):
        game = Game()
        arrangement = FenConverter.fen_converter(game, "R4B2/8/8/7K/k2N4/8/8/4Q3")
        util = GameStatusHandler(arrangement)
        self.assertEqual(util.is_stalemate(0), False)

    def test_six(self):
        game = Game()
        arrangement = FenConverter.fen_converter(game, "R4B2/8/8/7K/k2N4/8/8/4Q3")
        util = GameStatusHandler(arrangement)
        self.assertEqual(util.is_stalemate(1), False)
