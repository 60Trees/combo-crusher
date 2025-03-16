import sys

import control
import game_main as GAME
import pygame

if __name__ == "__main__":
    MNCTRL = control.Active_controls()
    control.reset_input(MNCTRL)

    # Initialise pygame
    pygame.init()
    pygame.font.init()
    
    WIN = pygame.display.set_mode((200, 200), pygame.RESIZABLE)
    pygame.display.set_caption("Combo Crusher")
    pygame.display.set_icon(pygame.image.load("main/assets/logo.png"))

    clock = pygame.time.Clock()
    done = False

    game = GAME.GAMECLASS.Game(WIN)

    # Main loop
    while not done:
        WIN.fill((255, 255, 255))

        control.prepare_input(MNCTRL)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                done = True
                pygame.quit()
                sys.exit()
            else:
                control.update_input(event, MNCTRL)
                game.GMCTRL = MNCTRL

        control.reset_input(MNCTRL)
        
        game.WIN = WIN

        GAME.draw_game(game)

        pygame.display.update(pygame.Rect(0, 0, WIN.get_width(), WIN.get_height()))
        clock.tick(60)

    # Quit pygame
    pygame.quit()
else:
    print(f'why tf is __name__ not "__main__" but instead "{__name__}"?!?!?!')
    input("Go on... seriously ! Thats not a rhetorical question. Why? --> ")