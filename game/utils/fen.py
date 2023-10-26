"""
fen.py
This module provides a utility class:
- `FenConverter` processes the FEN
"""

from models.bishop import Bishop
from models.king import King
from models.knight import Knight
from models.pawn import Pawn
from models.queen import Queen
from models.rook import Rook


class FenConverter:
    """
    Class to handle the Forsyth–Edwards Notation to describe a particular board position in the game.
    https://en.wikipedia.org/wiki/Forsyth%E2%80%93Edwards_Notation
    """

    piece_to_letter = {
        "p": Pawn,
        "r": Rook,
        "n": Knight,
        "b": Bishop,
        "q": Queen,
        "k": King,
    }

    @classmethod
    def fen_converter(cls, game, fen):
        """
        Converts a FEN string into a set of figures.

        Args:
            game (Game): The game that figures will be a part of.
            fen (str): The string with the FEN to be converted.

        Returns:
            set: A set of objects of figure subclasses.
        """

        rows = fen.split("/")
        figures = set()

        x, y = 0, 0
        for row in rows:
            for symbol in row:
                if symbol.isdigit():
                    x += int(symbol)
                    continue

                figures.add(cls.piece_to_letter[symbol.lower()](game, x, y, int(symbol.isupper())))
                x += 1

            x = 0
            y += 1

        return figures

    @classmethod
    def into_fen_converter(cls, figures):
        """
        Converts a given position on the board into a FEN.

        Args:
            figures (set): The set of figures representing the position to be converted into FEN.

        Returns:
            str: A string with the FEN.
        """
        fen = ""
        empty_count = 0

        for y in range(8):
            for x in range(8):
                square_empty = True
                for figure in figures:
                    if figure.x == x and figure.y == y:
                        square_empty = False
                        symbol = cls.piece_to_letter.get(type(figure), "")
                        if figure.color == 1:
                            symbol = symbol.upper()
                        fen += symbol

                if square_empty:
                    empty_count += 1
                else:
                    if empty_count > 0:
                        fen += str(empty_count)
                        empty_count = 0

            if empty_count > 0:
                fen += str(empty_count)
                empty_count = 0

            if y < 7:
                fen += "/"

        return fen
