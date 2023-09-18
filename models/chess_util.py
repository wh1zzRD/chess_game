from models.king import King


def create_new_arrangement(current_arrangement, figure_to_move, move):
    new_arrangement = []
    for figure in current_arrangement:
        if figure == figure_to_move:
            new_arrangement.append(type(figure)(figure.game, move[0], move[1], figure.color))
        else:
            new_arrangement.append(type(figure)(figure.game, figure.x, figure.y, figure.color))

    return new_arrangement


class ChessUtil:
    def __init__(self, arrangement):
        self.figures = arrangement.copy()

    def find_king_pos(self, given_side):
        for figure in self.figures:
            if isinstance(figure, King) and figure.color == given_side:
                return figure.x, figure.y

    def find_king(self, given_side):
        for figure in self.figures:
            if isinstance(figure, King) and figure.color == given_side:
                return figure

    def is_any_figure_in_coords(self, coords):
        for figure in self.figures:
            if figure.x == coords[0] and figure.y == coords[1]:
                return figure
        return None

    def get_moves(self, figure):
        possible_moves = figure.calculate_moves()
        legal_moves = []

        for direction in possible_moves:
            for move in direction:
                is_figure_in_way = self.is_any_figure_in_coords(move)
                if is_figure_in_way is not None:
                    if is_figure_in_way.color != figure.color:
                        legal_moves.append(move)
                    break
                legal_moves.append(move)

        return legal_moves

    def is_check(self, given_side):
        king_pos = self.find_king_pos(given_side)
        for figure in self.figures:
            if figure.color != given_side and king_pos in self.get_moves(figure):
                return True
        return False

    def is_mate(self, given_side):
        if self.is_check(given_side):
            for figure in self.figures:
                if figure.color == given_side:
                    for move in self.get_moves(figure):
                        new_arrangement = ChessUtil(create_new_arrangement(self.figures, figure, move))
                        if not new_arrangement.is_check(given_side):
                            return False
            return True
        return False

    def is_stalemate(self, given_side):
        if not self.is_check(given_side):
            for figure in self.figures:
                if figure.color == given_side:
                    for move in self.get_moves(figure):
                        new_arrangement = ChessUtil(create_new_arrangement(self.figures, figure, move))
                        if not new_arrangement.is_check(given_side):
                            return False
            return True
        return False

    def is_move_legal(self, figure, move):
        arrangement_after_move = ChessUtil(create_new_arrangement(self.figures, figure, move))
        if not arrangement_after_move.is_check(figure.color):
            return True
        return False
