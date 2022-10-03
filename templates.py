import pygame
from typing import Optional
from models import Game, Figure


if __name__ == "__main__":
    selected_figure: Optional[Figure] = None
    moves = []
    game = Game()

    while game.keep_doing:
        game.clock.tick(game.FPS)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                game.keep_doing = False

        # game.display.fill((218, 163, 120))
        game.display.fill((97, 53, 7))
        game.display_field()
        game.display_coordinates()

        # Displaying figures
        for figure in game.figures:
            figure.draw()

        # Displaying possible moves if there is a selected figure
        if selected_figure:
            selected_figure.display_possible_moves(moves)

        # Displaying the result and ending the game in case of checkmate
        game.check_mate()
        if game.mate:
            keep_doing = False
            break

        if event.type == pygame.MOUSEBUTTONDOWN:

            if event.button == 1:
                mouse_x, mouse_y = pygame.mouse.get_pos()
                mouse_x = (mouse_x - 35) // 100
                mouse_y = (mouse_y - 35) // 100

                if selected_figure:
                    if mouse_x == selected_figure.x and mouse_y == selected_figure.y:
                        selected_figure.deselect()
                        selected_figure = None
                        event.button = 0
                        continue
                    if selected_figure.move(mouse_x, mouse_y):
                        if game.pawn_switched_to_queen:
                            for figure in game.figures:
                                if [figure.x, figure.y] == [selected_figure.x, selected_figure.y]:
                                    selected_figure = figure
                                    game.pawn_switched_to_queen = False
                                    break
                        if selected_figure.check():
                            print("check")
                            if selected_figure.mate():
                                mate = True
                                print("mate")
                        game.turn = not selected_figure.color
                        selected_figure.deselect()
                        selected_figure = None
                        game.opponent_move = True
                        moves = []
                        continue

                for figure in game.figures:
                    if mouse_x == figure.x and mouse_y == figure.y and not selected_figure:
                        if figure.color == game.turn:
                            figure.set_as_selected()
                            moves = figure.remove_if_check()
                            selected_figure = figure
                            event.button = 0
                            break

        pygame.display.flip()

    pygame.quit()
