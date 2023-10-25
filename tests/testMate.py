import unittest

from game.utils.game_status_handler import GameStatusHandler
from game.utils.fen import FenConverter
from game.game import Game


class CheckmateTest(unittest.TestCase):

    def test_one(self):
        game = Game()
        arrangement = FenConverter.fen_converter(game, "rr6/8/8/7k/8/8/K7/8")
        util = GameStatusHandler(arrangement)
        self.assertEqual(util.is_mate(1), True)

    def test_two(self):
        game = Game()
        arrangement = FenConverter.fen_converter(game, "1rr5/8/8/7k/8/8/K7/8")
        util = GameStatusHandler(arrangement)
        self.assertEqual(util.is_mate(1), False)

    def test_three(self):
        game = Game()
        arrangement = FenConverter.fen_converter(game, "1rr5/8/8/7k/8/8/K7/8")
        util = GameStatusHandler(arrangement)
        self.assertEqual(util.is_mate(0), False)

    def test_four(self):
        game = Game()
        arrangement = FenConverter.fen_converter(game, "2KB4/3B1N2/8/7k/5N2/8/8/8")
        util = GameStatusHandler(arrangement)
        self.assertEqual(util.is_mate(0), True)

    def test_five(self):
        game = Game()
        arrangement = FenConverter.fen_converter(game, "2KB4/3B4/8/7k/5N2/8/8/8")
        util = GameStatusHandler(arrangement)
        self.assertEqual(util.is_mate(0), False)

    def test_six(self):
        game = Game()
        arrangement = FenConverter.fen_converter(game, "2KB4/3B4/8/7k/5N2/8/8/1qr5")
        util = GameStatusHandler(arrangement)
        self.assertEqual(util.is_mate(1), False)
