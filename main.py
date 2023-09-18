import pygame
# from models import Game
from models.game import Game


def main():
    game = Game()

    while game.keep_doing:
        game.clock.tick(game.FPS)

        game.display_field()
        game.display_coordinates()
        game.display_figures()

        # Displaying possible moves if there is a selected figure
        game.display_selected_figures_moves()

        # Displaying the result and ending the game in case of checkmate
        game.display_result()

        for event in pygame.event.get():
            game.process_exit_event(event)
            game.process_figure_handling_event(event)

        pygame.display.flip()

    pygame.quit()


if __name__ == "__main__":
    main()
