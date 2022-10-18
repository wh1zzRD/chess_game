import pygame
import time
from typing import Optional


class Game:

    def __init__(self):
        pygame.init()
        width, height = 870, 870
        self.FPS = 40
        self.display = pygame.display.set_mode((width, height))
        pygame.display.set_caption('Chess')
        self.clock = pygame.time.Clock()
        self.font = pygame.font.SysFont('Comic Sans MS', 30)

        self.pawn_switched_to_queen = False

        self.keep_doing = True
        self.check = False
        self.mate = False
        self.result = None
        self.turn = 1
        self.opponent_move = False
        self.figures = self.fen_converter()

    def fen_converter(self):
        fen = "rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR"
        # fen = "8/2q4N/4k3/2b5/2P5/1P3N1r/8/1R6"
        # fen = "8/2P5/8/k7/6q1/2Q5/5K2/8"

        rows = fen.split("/")
        figures = set()

        x, y = 0, 0
        for row in rows:
            for symbol in row:
                if symbol == "p":
                    figures.add(Pawn(self, x, y, 0))
                elif symbol == "P":
                    figures.add(Pawn(self, x, y, 1))
                elif symbol == "r":
                    figures.add(Rook(self, x, y, 0))
                elif symbol == "R":
                    figures.add(Rook(self, x, y, 1))
                elif symbol == "n":
                    figures.add(Knight(self, x, y, 0))
                elif symbol == "N":
                    figures.add(Knight(self, x, y, 1))
                elif symbol == "b":
                    figures.add(Bishop(self, x, y, 0))
                elif symbol == "B":
                    figures.add(Bishop(self, x, y, 1))
                elif symbol == "q":
                    figures.add(Queen(self, x, y, 0))
                elif symbol == "Q":
                    figures.add(Queen(self, x, y, 1))
                elif symbol == "k":
                    figures.add(King(self, x, y, 0))
                elif symbol == "K":
                    figures.add(King(self, x, y, 1))

                if symbol.isdigit():
                    x += int(symbol)
                    continue
                x += 1

            x = 0
            y += 1

        return figures

    def display_field(self):
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

    def check_mate(self):
        if self.mate:
            self.result = "checkmate"
            check_image = self.font.render("Result: " + str(self.result), True, (120, 218, 127))
            self.display.blit(check_image, (300, 400))
            pygame.display.update()
            time.sleep(3)
            pygame.quit()


# parent class for every figure

class Figure:

    @property
    def picture_white(self):
        raise NotImplementedError()

    @property
    def picture_black(self):
        raise NotImplementedError()

    # When creating a figure: passing game object, position on the board and color.
    # Figure gets an image assigned from its own class
    def __init__(self, game, x, y, color):  # TODO change parameters x, y to tuple
        self.game = game
        self.x = x
        self.y = y
        self.color = color
        self.is_selected = False
        if color:
            self.image = pygame.transform.rotozoom(self.picture_white, 0, 0.4)
            self.factor = 1
        else:
            self.image = pygame.transform.rotozoom(self.picture_black, 0, 0.4)
            self.factor = -1

    def __repr__(self):
        raise NotImplementedError

    def draw(self):
        self.game.display.blit(self.image, (self.x * 100 + 35, self.y * 100 + 35))

    # Making the figure bigger if it's selected
    def set_as_selected(self):
        if self.is_selected:
            return
        self.is_selected = True
        self.image = pygame.transform.rotozoom(self.image, 0, 1.1)

    def deselect(self):
        self.is_selected = False
        if self.color:
            self.image = pygame.transform.rotozoom(self.picture_white, 0, 0.4)
        else:
            self.image = pygame.transform.rotozoom(self.picture_black, 0, 0.4)

    def move(self, mouse_x, mouse_y):  # TODO change mouse coordinates to a tuple

        mouse_coordinates = [mouse_x, mouse_y]  # Coordinates of a field, where user  tries to move the figure
        figure_to_delete: Optional[Figure] = None

        if mouse_coordinates in self.remove_if_check():  # If the field is a possible move for this figure
            deleting = False

            for figure in self.game.figures:
                # If there is another figure in the field where we try to move our figure
                if [figure.x, figure.y] == mouse_coordinates and figure.color != self.color:
                    figure_to_delete = figure
                    deleting = True
                    break
            if deleting:
                self.game.figures.remove(figure_to_delete)
            self.x, self.y = mouse_coordinates
            # Turning Pawn into Queen if its on the end of the board
            if isinstance(self, Pawn) and ((self.y == 0 and self.color == 1) or (self.y == 7 and self.color == 0)):
                self.pawn_to_queen()
                self.game.pawn_switched_to_queen = True
            return True
        else:
            return False

    def display_possible_moves(self, moves):
        # Displaying a circle on every field on the board that is a possible move for the figure
        for move in moves:
            pygame.draw.circle(self.game.display, (80, 80, 80), (move[0] * 100 + 85, move[1] * 100 + 85), 20)

        # Drawing figures once more, so they are over the circles for moves
        for figure in self.game.figures:
            figure.draw()

    def calculate_moves(self):
        raise NotImplementedError("This method should be implemented in child classes")

    def remove_if_check(self):
        """
        If a move in possible moves will lead to a check after your move, respectively to checkmate for you on
        opponent's move, such move is removed from possible moves
        """
        prev_x = self.x
        prev_y = self.y
        possible_moves = self.calculate_moves()
        check_found = False
        valid_moves = []

        king_pos = None
        for figure in self.game.figures:
            if isinstance(figure, King) and figure.color == self.color:
                king_pos = [figure.x, figure.y]

        if not isinstance(self, King):
            for move in possible_moves:
                self.x, self.y = move
                beaten_figure: Optional[Figure] = None

                for figure in self.game.figures:
                    if [figure.x, figure.y] == move and figure.color != self.color:
                        beaten_figure = figure

                for figure in self.game.figures:
                    if check_found:  # Move is invalid of eve one of opponent's figures will beat your king after
                        break

                    if figure.color != self.color and figure != beaten_figure:
                        if king_pos in figure.calculate_moves():
                            check_found = True
                            break

                self.x = prev_x
                self.y = prev_y
                beaten_figure = None

                if check_found:
                    check_found = False
                    continue

                valid_moves.append(move)
        else:
            """
            If the figure we are moving is the king, we have to consider its position after a move and not before, 
            when checking for check
            """
            for move in possible_moves:
                self.x, self.y = move
                beaten_figure = None

                for figure in self.game.figures:
                    if [figure.x, figure.y] == move and figure.color != self.color:
                        beaten_figure = figure

                for figure in self.game.figures:
                    if check_found:
                        break

                    if figure.color != self.color and figure != beaten_figure:
                        if move in figure.calculate_moves():
                            check_found = True
                            break

                self.x = prev_x
                self.y = prev_y
                beaten_figure = None

                if check_found:
                    check_found = False
                    continue

                valid_moves.append(move)

        return valid_moves

    def check(self):
        king_pos = None
        for figure in self.game.figures:
            if isinstance(figure, King) and figure.color != self.color:
                king_pos = [figure.x, figure.y]
                break

        for figure in self.game.figures:
            if figure.color == self.color:
                if king_pos in figure.calculate_moves():
                    return True

    def mate(self):
        for figure in self.game.figures:
            if figure.color != self.color:
                if figure.remove_if_check():
                    return False

        return True


# class for each figure

class Pawn(Figure):
    picture_white = pygame.image.load('img/pawn.png')
    picture_black = pygame.image.load('img/black_pawn.png')

    def calculate_moves(self):
        possible_moves = []

        figure_in_front = False
        figure_two_in_front = False

        for figure in self.game.figures:

            if figure.x == self.x and figure.y + 1 * self.factor == self.y:
                figure_in_front = True

            if figure.x == self.x and figure.y + 2 * self.factor == self.y:
                figure_two_in_front = True

            if figure.y + 1 * self.factor == self.y and (
                    figure.x + 1 * self.factor == self.x or figure.x - 1 * self.factor == self.x) and figure.color != self.color:
                possible_moves.append([figure.x, figure.y])

        if ((self.y == 6 and self.color == 1) or (self.y == 1 and self.color == 0)) and (
                not figure_two_in_front and not figure_in_front):
            possible_moves.append([self.x, self.y - 2 * self.factor])

        if not figure_in_front:
            possible_moves.append([self.x, self.y - 1 * self.factor])

        return possible_moves

    def __repr__(self):
        return f"Pawn_Object_at_{self.x}/{self.y}"

    def pawn_to_queen(self):
        # queen = Queen(self, self.x, self.y, self.color)
        self.game.figures.add(Queen(self.game, self.x, self.y, self.color))
        self.game.figures.remove(self)
        # self.game.figures.add(queen)


class King(Figure):
    picture_white = pygame.image.load('img/king.png')
    picture_black = pygame.image.load('img/black_king.png')

    def calculate_moves(self):
        possible_moves = [[self.x, self.y + 1], [self.x, self.y - 1], [self.x + 1, self.y], [self.x - 1, self.y],
                          [self.x + 1, self.y - 1], [self.x + 1, self.y + 1], [self.x - 1, self.y + 1],
                          [self.x - 1, self.y - 1]]
        possible_moves_end = []

        for figure in self.game.figures:
            for i in possible_moves:
                if [figure.x, figure.y] == i and figure.color == self.color:
                    possible_moves.remove(i)

        for move in possible_moves:
            if move[0] < 0 or move[0] > 7 or move[1] < 0 or move[1] > 7:
                continue
            else:
                possible_moves_end.append(move)

        return possible_moves_end

    def __repr__(self):
        return f"King Object at {self.x} {self.y}"


class Rook(Figure):
    picture_white = pygame.image.load('img/rook.png')
    picture_black = pygame.image.load('img/black_rook.png')

    def calculate_moves(self):
        possible_moves = []
        possible_moves_end = []
        figure_found = False

        for y in range(self.y - 1, -1, -1):
            for figure in self.game.figures:
                if figure.x == self.x and figure.y == y:
                    if figure.color == self.color:
                        figure_found = True
                        break
                    else:
                        figure_found = True
                        possible_moves.append([figure.x, figure.y])
            if figure_found:
                figure_found = False
                break
            possible_moves.append([self.x, y])

        for y in range(self.y + 1, 8):
            for figure in self.game.figures:
                if figure.x == self.x and figure.y == y:
                    if figure.color == self.color:
                        figure_found = True
                        break
                    else:
                        figure_found = True
                        possible_moves.append([figure.x, figure.y])
            if figure_found:
                figure_found = False
                break
            possible_moves.append([self.x, y])

        for x in range(self.x - 1, -1, -1):
            for figure in self.game.figures:
                if figure.y == self.y and figure.x == x:
                    if figure.color == self.color:
                        figure_found = True
                        break
                    else:
                        figure_found = True
                        possible_moves.append([figure.x, figure.y])
            if figure_found:
                figure_found = False
                break
            possible_moves.append([x, self.y])

        for x in range(self.x + 1, 8):
            for figure in self.game.figures:
                if figure.y == self.y and figure.x == x:
                    if figure.color == self.color:
                        figure_found = True
                        break
                    else:
                        figure_found = True
                        possible_moves.append([figure.x, figure.y])
            if figure_found:
                figure_found = False
                break
            possible_moves.append([x, self.y])

        for move in possible_moves:
            if move[0] < 0 or move[0] > 7 or move[1] < 0 or move[1] > 7:
                continue
            else:
                possible_moves_end.append(move)

        return possible_moves_end

    def __repr__(self):
        return f"Rook_Object_at_{self.x} /{self.y}"


class Bishop(Figure):
    picture_white = pygame.image.load('img/bishop.png')
    picture_black = pygame.image.load('img/black_bishop.png')

    def calculate_moves(self):
        possible_moves = []
        possible_moves_end = []
        figure_found = False

        for i in range(1, 8):
            if self.x + i > 7 or self.y + i > 7:
                break

            for figure in self.game.figures:
                if figure.x == self.x + i and figure.y == self.y + i:
                    if figure.color == self.color:
                        figure_found = True
                        break
                    else:
                        figure_found = True
                        possible_moves.append([figure.x, figure.y])
                        break

            if figure_found:
                figure_found = False
                break
            possible_moves.append([self.x + i, self.y + i])

        for i in range(1, 8):
            if self.x + i > 7 or self.y - i > 7:
                break

            for figure in self.game.figures:
                if figure.x == self.x + i and figure.y == self.y - i:
                    if figure.color == self.color:
                        figure_found = True
                        break
                    else:
                        figure_found = True
                        possible_moves.append([figure.x, figure.y])
                        break

            if figure_found:
                figure_found = False
                break
            possible_moves.append([self.x + i, self.y - i])

        for i in range(1, 8):
            if self.x - i > 7 or self.y + i > 7:
                break

            for figure in self.game.figures:
                if figure.x == self.x - i and figure.y == self.y + i:
                    if figure.color == self.color:
                        figure_found = True
                        break
                    else:
                        figure_found = True
                        possible_moves.append([figure.x, figure.y])
                        break

            if figure_found:
                figure_found = False
                break
            possible_moves.append([self.x - i, self.y + i])

        for i in range(1, 8):
            if self.x - i > 7 or self.y - i > 7:
                break

            for figure in self.game.figures:
                if figure.x == self.x - i and figure.y == self.y - i:
                    if figure.color == self.color:
                        figure_found = True
                        break
                    else:
                        figure_found = True
                        possible_moves.append([figure.x, figure.y])
                        break

            if figure_found:
                figure_found = False
                break
            possible_moves.append([self.x - i, self.y - i])

        for move in possible_moves:
            if move[0] < 0 or move[0] > 7 or move[1] < 0 or move[1] > 7:
                continue
            else:
                possible_moves_end.append(move)

        return possible_moves_end

    def __repr__(self):
        return f"Bishop_Object_at_{self.x}/{self.y}"


class Knight(Figure):
    picture_white = pygame.image.load('img/knight.png')
    picture_black = pygame.image.load('img/black_knight.png')

    def calculate_moves(self):
        possible_moves = [[self.x - 1, self.y - 2], [self.x + 1, self.y + 2], [self.x - 2, self.y - 1],
                          [self.x - 2, self.y + 1], [self.x - 1, self.y + 2], [self.x + 1, self.y - 2],
                          [self.x + 2, self.y - 1], [self.x + 2, self.y + 1]]
        possible_moves_end = []

        for figure in self.game.figures:
            for i in possible_moves:
                if figure.color == self.color and [figure.x, figure.y] == i:
                    possible_moves.remove(i)

        for move in possible_moves:
            if move[0] < 0 or move[0] > 7 or move[1] < 0 or move[1] > 7:
                continue
            else:
                possible_moves_end.append(move)

        return possible_moves_end

    def __repr__(self):
        return f"Knight_Object_at_{self.x}/{self.y}"


class Queen(Figure):
    picture_white = pygame.image.load('img/queen.png')
    picture_black = pygame.image.load('img/black_queen.png')

    def calculate_moves(self):
        possible_moves = []
        possible_moves_end = []
        figure_found = False

        for y in range(self.y - 1, -1, -1):
            for figure in self.game.figures:
                if figure.x == self.x and figure.y == y:
                    if figure.color == self.color:
                        figure_found = True
                        break
                    else:
                        figure_found = True
                        possible_moves.append([figure.x, figure.y])
            if figure_found:
                figure_found = False
                break
            possible_moves.append([self.x, y])

        for y in range(self.y + 1, 8):
            for figure in self.game.figures:
                if figure.x == self.x and figure.y == y:
                    if figure.color == self.color:
                        figure_found = True
                        break
                    else:
                        figure_found = True
                        possible_moves.append([figure.x, figure.y])
            if figure_found:
                figure_found = False
                break
            possible_moves.append([self.x, y])

        for x in range(self.x - 1, -1, -1):
            for figure in self.game.figures:
                if figure.y == self.y and figure.x == x:
                    if figure.color == self.color:
                        figure_found = True
                        break
                    else:
                        figure_found = True
                        possible_moves.append([figure.x, figure.y])
            if figure_found:
                figure_found = False
                break
            possible_moves.append([x, self.y])

        for x in range(self.x + 1, 8):
            for figure in self.game.figures:
                if figure.y == self.y and figure.x == x:
                    if figure.color == self.color:
                        figure_found = True
                        break
                    else:
                        figure_found = True
                        possible_moves.append([figure.x, figure.y])
            if figure_found:
                figure_found = False
                break
            possible_moves.append([x, self.y])

        for i in range(1, 8):
            if self.x + i > 7 or self.y + i > 7:
                break
            for figure in self.game.figures:
                if figure.x == self.x + i and figure.y == self.y + i:
                    if figure.color == self.color:
                        figure_found = True
                        break
                    else:
                        figure_found = True
                        possible_moves.append([figure.x, figure.y])
                        break
            if figure_found:
                figure_found = False
                break
            possible_moves.append([self.x + i, self.y + i])

        for i in range(1, 8):
            if self.x + i > 7 or self.y - i > 7:
                break
            for figure in self.game.figures:
                if figure.x == self.x + i and figure.y == self.y - i:
                    if figure.color == self.color:
                        figure_found = True
                        break
                    else:
                        figure_found = True
                        possible_moves.append([figure.x, figure.y])
                        break
            if figure_found:
                figure_found = False
                break
            possible_moves.append([self.x + i, self.y - i])

        for i in range(1, 8):
            if self.x - i > 7 or self.y + i > 7:
                break
            for figure in self.game.figures:
                if figure.x == self.x - i and figure.y == self.y + i:
                    if figure.color == self.color:
                        figure_found = True
                        break
                    else:
                        figure_found = True
                        possible_moves.append([figure.x, figure.y])
                        break
            if figure_found:
                figure_found = False
                break
            possible_moves.append([self.x - i, self.y + i])

        for i in range(1, 8):
            if self.x - i > 7 or self.y - i > 7:
                break
            for figure in self.game.figures:
                if figure.x == self.x - i and figure.y == self.y - i:
                    if figure.color == self.color:
                        figure_found = True
                        break
                    else:
                        figure_found = True
                        possible_moves.append([figure.x, figure.y])
                        break

            if figure_found:
                figure_found = False
                break
            possible_moves.append([self.x - i, self.y - i])

        for move in possible_moves:
            if move[0] < 0 or move[0] > 7 or move[1] < 0 or move[1] > 7:
                continue
            else:
                possible_moves_end.append(move)

        return possible_moves_end

    def __repr__(self):
        return f"Queen_Object_at_{self.x}/{self.y}"
