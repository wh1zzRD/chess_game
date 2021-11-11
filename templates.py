import pygame
import time
import random

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

        if mouse_coordinates in self.remove_if_check():
            deleting = False

            for figure in figures:
                if [figure.x, figure.y] == mouse_coordinates and figure.color != self.color:
                    figure_to_delete = figure
                    deleting = True
                    break
            if deleting:
                figures.remove(figure_to_delete)
            self.x, self.y = mouse_coordinates
            if isinstance(self, Pawn) and ((self.y == 0 and self.color == 1) or (self.y == 7 and self.color == 0)):
                self.pawn_to_queen()
            return True
        else:
            return False

    def display_possible_moves(self):
        for move in self.remove_if_check():
            pygame.draw.rect(display, (80, 80, 80), (move[0] * 100 + 10, move[1] * 100 + 10, 80, 80))

        for figure in figures:
            figure.draw(display)

    def remove_if_check(self):
        prev_x = self.x
        prev_y = self.y
        possible_moves = self.calculate_moves()
        check_found = False
        moves_to_remove = []

        king_pos = None
        for figure in figures:
            if isinstance(figure, King) and figure.color == self.color:
                king_pos = [figure.x, figure.y]
                break

        for move in possible_moves:
            self.x = move[0]
            self.y = move[1]
            beaten_figure = None

            for figure in figures:
                if [figure.x, figure.y] == move and figure.color != self.color:
                    beaten_figure = figure
            
            for figure in figures:
                if check_found:
                    check_found = False
                    break

                if isinstance(self, King):
                    if figure.color != self.color and figure != beaten_figure:
                        if [self.x, self.y] in figure.calculate_moves():
                            moves_to_remove.append(move)
                else:
                    if figure.color != self.color and figure != beaten_figure:
                        if king_pos in figure.calculate_moves():
                            moves_to_remove.append(move)
                            check = True
                            break

            self.x = prev_x
            self.y = prev_y
            beaten_figure = None

        if moves_to_remove:
            for move_to_remove in moves_to_remove:
                try:
                    possible_moves.remove(move_to_remove)
                except:
                    continue

        return possible_moves

    def check(self):
        king_pos = None
        for figure in figures:
            if isinstance(figure, King) and figure.color != self.color:
                king_pos = [figure.x, figure.y]
                break

        for figure in figures:
            if figure.color == self.color:
                # for i in figure.calculate_moves():
                #     if i == king_pos:
                #         return True
                if king_pos in figure.calculate_moves():
                    return True

    def mate(self):
        for figure in figures:
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

        for figure in figures:

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

    def pawn_to_queen(self):
        figures.add(Queen(self.x, self.y, self.color))
        figures.remove(self)


class King(Figure):
    picture_white = pygame.image.load('img/king.png')
    picture_black = pygame.image.load('img/black_king.png')

    def calculate_moves(self):
        possible_moves = [[self.x, self.y + 1], [self.x, self.y - 1], [self.x + 1, self.y], [self.x - 1, self.y],
                          [self.x + 1, self.y - 1], [self.x + 1, self.y + 1], [self.x - 1, self.y + 1],
                          [self.x - 1, self.y - 1]]

        for figure in figures:
            for i in possible_moves:
                if [figure.x, figure.y] == i and figure.color == self.color:
                    possible_moves.remove(i)

        for move in possible_moves:
            if move[0] > 7 or move[1] > 7 or move[0] < 0 or move[1] < 0:
                possible_moves.remove(move)

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

        for move in possible_moves:
            if move[0] > 7 or move[1] > 7 or move[0] < 0 or move[1] < 0:
                possible_moves.remove(move)

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

        
        for move in possible_moves:
            if move[0] > 7 or move[1] > 7 or move[0] < 0 or move[1] < 0:
                possible_moves.remove(move)


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

        for move in possible_moves:
            if move[0] > 7 or move[1] > 7 or move[0] < 0 or move[1] < 0:
                possible_moves.remove(move)

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

        for move in possible_moves:
            if move[0] > 7 or move[1] > 7 or move[0] < 0 or move[1] < 0:
                possible_moves.remove(move)

        return possible_moves

# global variables will be here

figures = {Rook(0, 0, 0), Knight(1, 0, 0), Bishop(2, 0, 0), Queen(3, 0, 0), King(4, 0, 0), Bishop(5, 0, 0), Knight(6, 0, 0), Rook(7, 0, 0),
           Pawn(0, 1, 0), Pawn(1, 1, 0), Pawn(2, 1, 0), Pawn(3, 1, 0), Pawn(4, 1, 0), Pawn(5, 1, 0), Pawn(6, 1, 0), Pawn(7, 1, 0),
           Pawn(0, 6, 1), Pawn(1, 6, 1), Pawn(2, 6, 1), Pawn(3, 6, 1), Pawn(4, 6, 1), Pawn(5, 6, 1), Pawn(6, 6, 1), Pawn(7, 6, 1),
           Rook(0, 7, 1), Knight(1, 7, 1), Bishop(2, 7, 1), Queen(4, 7, 1), King(3, 7, 1), Bishop(5, 7, 1), Knight(6, 7, 1), Rook(7, 7, 1)}

selected_figure = None
turn = 1

opponent_move = False

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
        color = (97, 53, 7)
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

    if selected_figure:
        selected_figure.display_possible_moves()

    if mate:
        result = "checkmate"
        check_image = font.render("Result: " + str(result), True, (120, 218, 127))
        display.blit(check_image, (300, 400))
        pygame.display.update()
        time.sleep(3)
        pygame.quit()
    
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
                            mate = True
                            print("mate")
                    turn = not selected_figure.color
                    selected_figure.deselect()
                    selected_figure = None
                    opponent_move = True
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
