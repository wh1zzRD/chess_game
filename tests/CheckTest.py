import unittest
import os
import shutil

from models.chess_util import ChessUtil
from models.fen import FenConverter
from models.game import Game


class CheckTest(unittest.TestCase):

    def setUp(self) -> None:
        # source_folder = r"E:/chess_game/img/"
        # destination_folder = r"E:/chess_game/tests/img/"
        #
        # if not os.path.exists(destination_folder):
        #     os.makedirs(destination_folder)
        #
        # # fetch all files
        # for file_name in os.listdir(source_folder):
        #     # construct full file path
        #     source = source_folder + file_name
        #     destination = destination_folder + file_name
        #     # copy only files
        #     if os.path.isfile(source):
        #         shutil.copy(source, destination)
        pass
        # TODO add setUp and tearDown

    def tearDown(self) -> None:
        # shutil.rmtree(r"E:/chess_game/tests/img/")
        pass

    def test_one(self):
        game = Game()
        arrangement = FenConverter.fen_converter(game, "3rr3/8/8/7k/3K4/8/8/8")
        util = ChessUtil(arrangement)
        self.assertEqual(util.is_check(1), True)

    def test_two(self):
        game = Game()
        arrangement = FenConverter.fen_converter(game, "3rr3/8/8/7k/3K4/8/8/3Q4")
        util = ChessUtil(arrangement)
        self.assertEqual(util.is_check(0), True)

    def test_three(self):
        game = Game()
        arrangement = FenConverter.fen_converter(game, "4K3/8/8/8/8/8/8/3k4")
        util = ChessUtil(arrangement)
        self.assertEqual(util.is_check(1), False)

    def test_four(self):
        game = Game()
        arrangement = FenConverter.fen_converter(game, "4K3/3R4/8/7B/8/8/8/3k4")
        util = ChessUtil(arrangement)
        self.assertEqual(util.is_check(0), True)

    def test_five(self):
        game = Game()
        arrangement = FenConverter.fen_converter(game, "4K3/2R5/7B/8/8/8/8/3k4")
        util = ChessUtil(arrangement)
        self.assertEqual(util.is_check(0), False)
