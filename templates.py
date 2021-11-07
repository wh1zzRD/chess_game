import pygame
import time

pygame.init()
width, height = 800, 800
FPS = 40
display = pygame.display.set_mode((width, height))

keep_doing = True
clock = pygame.time.Clock()

font = pygame.font.SysFont('Comic Sans MS', 30)

# parent class for every figure

class Figure:

    def __init__(self, x, y, color):
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

    def draw(self, display):
        display.blit(self.image, (self.x * 100, self.y * 100))

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

    def move(self, mouse_x, mouse_y):
        mouse_coordinates = [mouse_x, mouse_y]
        possible_moves = self.calculate_moves()
        for i in possible_moves:
            if mouse_coordinates == i:
                for figure in figures:
                    if [figure.x, figure.y] == i and figure.color != self.color:
                        figures.remove(figure)
                        break
                prev_x = self.x
                prev_y = self.y
                self.x = i[0]
                self.y = i[1]
                if self.avoid_checkmate():
                    self.x = prev_x
                    self.y = prev_y
                    return False
                return True
        return False

    def avoid_checkmate(self):
        king_pos = None
        for figure in figures:
            if isinstance(figure, King) and figure.color == turn:
                king_pos = [figure.x, figure.y]
                break

        for figure in figures:
            if figure.color != turn:
                for i in figure.calculate_moves():
                    if i == king_pos:
                        print("you have to avoid checkmate")
                        return True

    def check(self):
        king_pos = None
        for figure in figures:
            if isinstance(figure, King) and figure.color != turn:
                king_pos = [figure.x, figure.y]
                break

        for figure in figures:
            if figure.color == turn:
                for i in figure.calculate_moves():
                    if i == king_pos:
                        return True

    def mate(self):
        # king_position = None
        there_is_possible_move = False
        # for figure in figures:
        #     if isinstance(figure, King) and figure.color != turn:
        #         king_position = [figure.x, figure.y]
        #         break

        for figure in figures:
            if there_is_possible_move:
                return False

            if figure.color != turn:
                prev_x = figure.x
                prev_y = figure.y
                for i in figure.calculate_moves():
                    figure.x = i[0]
                    figure.y = i[1]
                    if figure.check():
                        figure.x = prev_x
                        figure.y = prev_y
                    else:
                        there_is_possible_move = True
                        figure.x = prev_x
                        figure.y = prev_y
                        break

        return True

# class for each figure

class Pawn(Figure):
    picture_white = pygame.image.load('img/pawn.png')
    picture_black = pygame.image.load('img/black_pawn.png')

    def calculate_moves(self):
        possible_moves = []

        figure_in_front = False
        figure_two_in_front = False

        for figure in figures:

            if figure.x == self.x and figure.y + 1 * self.factor == self.y:
                figure_in_front = True

            if figure.x == self.x and figure.y + 2 * self.factor == self.y:
                figure_two_in_front = True

            if figure.y + 1 * self.factor == self.y and (
                    figure.x + 1 * self.factor == self.x or figure.x - 1 * self.factor == self.x) and figure.color != self.color:
                possible_moves.append([figure.x, figure.y])

        if ((self.y == 6 and self.color == 1) or (self.y == 1 and self.color == 0)) and (
                not figure_two_in_front or not figure_in_front):
            possible_moves.append([self.x, self.y - 2 * self.factor])

        if not figure_in_front:
            possible_moves.append([self.x, self.y - 1 * self.factor])

        return possible_moves


class King(Figure):
    picture_white = pygame.image.load('img/king.png')
    picture_black = pygame.image.load('img/black_king.png')

    def calculate_moves(self):
        possible_moves = [[self.x, self.y + 1], [self.x, self.y - 1], [self.x + 1, self.y], [self.x - 1, self.y],
                          [self.x + 1, self.y - 1], [self.x + 1, self.y + 1], [self.x - 1, self.y + 1],
                          [self.x - 1, self.y - 1]]

        for figure in figures:
            for i in possible_moves:
                if figure.color == self.color and [figure.x, figure.y] == i:
                    possible_moves.remove(i)

        return possible_moves


class Rook(Figure):
    picture_white = pygame.image.load('img/rook.png')
    picture_black = pygame.image.load('img/black_rook.png')

    def calculate_moves(self):
        possible_moves = []
        figure_found = False

        for y in range(self.y - 1, -1, -1):
            for figure in figures:
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
            for figure in figures:
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
            for figure in figures:
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
            for figure in figures:
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

        return possible_moves


class Bishop(Figure):
    picture_white = pygame.image.load('img/bishop.png')
    picture_black = pygame.image.load('img/black_bishop.png')

    def calculate_moves(self):
        possible_moves = []
        figure_found = False

        for i in range(1, 8):
            if self.x + i > 7 or self.y + i > 7:
                break

            for figure in figures:
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

            for figure in figures:
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

            for figure in figures:
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

            for figure in figures:
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


        return possible_moves


class Knight(Figure):
    picture_white = pygame.image.load('img/knight.png')
    picture_black = pygame.image.load('img/black_knight.png')

    def calculate_moves(self):
        possible_moves = [[self.x - 1, self.y - 2], [self.x + 1, self.y + 2], [self.x - 2, self.y - 1],
                          [self.x - 2, self.y + 1], [self.x - 1, self.y + 2], [self.x + 1, self.y - 2],
                          [self.x + 2, self.y - 1], [self.x + 2, self.y + 1]]

        for figure in figures:
            for i in possible_moves:
                if figure.color == self.color and [figure.x, figure.y] == i:
                    possible_moves.remove(i)

        return possible_moves


class Queen(Figure):
    picture_white = pygame.image.load('img/queen.png')
    picture_black = pygame.image.load('img/black_queen.png')

    def calculate_moves(self):
        possible_moves = []
        figure_found = False

        for y in range(self.y - 1, -1, -1):
            for figure in figures:
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
            for figure in figures:
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
            for figure in figures:
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
            for figure in figures:
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
            for figure in figures:
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
            for figure in figures:
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
            for figure in figures:
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
            for figure in figures:
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

        return possible_moves

# global variables will be here

figures = {Rook(0, 0, 0), Knight(1, 0, 0), Bishop(2, 0, 0), Queen(3, 0, 0), King(4, 0, 0), Bishop(5, 0, 0), Knight(6, 0, 0), Rook(7, 0, 0),
           Pawn(0, 1, 0), Pawn(1, 1, 0), Pawn(2, 1, 0), Pawn(3, 1, 0), Pawn(4, 1, 0), Pawn(5, 1, 0), Pawn(6, 1, 0), Pawn(7, 1, 0),
           Pawn(0, 6, 1), Pawn(1, 6, 1), Pawn(2, 6, 1), Pawn(3, 6, 1), Pawn(4, 6, 1), Pawn(5, 6, 1), Pawn(6, 6, 1), Pawn(7, 6, 1),
           Rook(0, 7, 1), Knight(1, 7, 1), Bishop(2, 7, 1), Queen(3, 7, 1), King(4, 7, 1), Bishop(5, 7, 1), Knight(6, 7, 1), Rook(7, 7, 1)}

selected_figure = None
turn = 1

check = False
mate = False
result = None

# main game loop

while keep_doing:
    clock.tick(FPS)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            keep_doing = False

    display.fill((218, 163, 120))

    x_field_position = 0
    y_field_position = 0

    for i in range(32):
        color = (0, 0, 0)
        pygame.draw.rect(display, color, pygame.Rect(x_field_position, y_field_position, 100, 100))

        x_field_position += 200
        if x_field_position == 800:
            x_field_position = 100
            y_field_position += 100

        elif x_field_position == 900:
            x_field_position = 0
            y_field_position += 100

    for figure in figures:
        figure.draw(display)

    if result == "checkmate":
        check_image = font.render("Result: " + str(result), True, (120, 218, 127))
        display.blit(check_image, (300, 400))
        pygame.display.update()
        time.sleep(3)
        quit()

    if event.type == pygame.MOUSEBUTTONDOWN:

        if event.button == 1:
            mouse_x, mouse_y = pygame.mouse.get_pos()
            mouse_x //= 100
            mouse_y //= 100
            if selected_figure:
                if mouse_x == selected_figure.x and mouse_y == selected_figure.y:
                    selected_figure.deselect()
                    selected_figure = None
                    event.button = 0
                    continue
                if selected_figure.move(mouse_x, mouse_y):
                    if selected_figure.check():
                        print("check")
                    if selected_figure.mate():
                        result = "checkmate"
                        print(result)
                    turn = not selected_figure.color
                    selected_figure.deselect()
                    selected_figure = None
                    continue
            for figure in figures:
                if mouse_x == figure.x and mouse_y == figure.y and not selected_figure:
                    if figure.color == turn:
                        figure.set_as_selected()
                        selected_figure = figure

                        event.type != pygame.MOUSEBUTTONDOWN
                        event.button = 0
                        break

    pygame.display.flip()

pygame.quit()
