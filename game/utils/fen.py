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
    @staticmethod
    def fen_converter(game, fen):
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
                if symbol == "p":
                    figures.add(Pawn(game, x, y, 0))
                elif symbol == "P":
                    figures.add(Pawn(game, x, y, 1))
                elif symbol == "r":
                    figures.add(Rook(game, x, y, 0))
                elif symbol == "R":
                    figures.add(Rook(game, x, y, 1))
                elif symbol == "n":
                    figures.add(Knight(game, x, y, 0))
                elif symbol == "N":
                    figures.add(Knight(game, x, y, 1))
                elif symbol == "b":
                    figures.add(Bishop(game, x, y, 0))
                elif symbol == "B":
                    figures.add(Bishop(game, x, y, 1))
                elif symbol == "q":
                    figures.add(Queen(game, x, y, 0))
                elif symbol == "Q":
                    figures.add(Queen(game, x, y, 1))
                elif symbol == "k":
                    figures.add(King(game, x, y, 0))
                elif symbol == "K":
                    figures.add(King(game, x, y, 1))

                if symbol.isdigit():
                    x += int(symbol)
                    continue
                x += 1

            x = 0
            y += 1

        return figures

    @staticmethod
    def into_fen_converter(figures):
        """
        Converts a given position on the board into a FEN.

        Args:
            figures (set): The set of figures representing the position to be converted into FEN.

        Returns:
            str: A string with the FEN.
        """
        fen = ""
        current_symbol = ""
        counter = 0

        for y in range(8):
            for x in range(8):
                figure_found = False
                for figure in figures:
                    if [figure.x, figure.y] == [x, y]:
                        figure_found = True
                        if isinstance(figure, Pawn):
                            current_symbol = "p"
                        elif isinstance(figure, Queen):
                            current_symbol = "q"
                        elif isinstance(figure, Bishop):
                            current_symbol = "b"
                        elif isinstance(figure, King):
                            current_symbol = "k"
                        elif isinstance(figure, Knight):
                            current_symbol = "n"
                        elif isinstance(figure, Rook):
                            current_symbol = "r"

                        if figure.color == 1:
                            current_symbol = current_symbol.upper()

                        if counter:
                            fen += str(counter)
                            counter = 0

                        fen += current_symbol

                if not figure_found:
                    counter += 1

            if counter:
                fen += str(counter)
                counter = 0
            fen += "/"

        return fen[:-1]
