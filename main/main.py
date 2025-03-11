
import sys
import pygame

import game_main as GAME

if __name__ == "__main__":
    # Initialise pygame
    pygame.init()
    pygame.font.init()

    clock = pygame.time.Clock()

    WIN = pygame.display.set_mode((200, 200), pygame.RESIZABLE)

    pygame.display.set_caption("Combo Crusher")

    done = False

    pygame.display.set_icon(pygame.image.load("main/assets/logo.png"))

    GAME.start_game(WIN)

    # Main loop
    while not done:
        WIN.fill((255, 255, 255))
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                done = True
                pygame.quit()
                sys.exit()
            else:
                GAME.control.update_input(event)

        GAME.draw_game(WIN)

        pygame.display.update(pygame.Rect(0, 0, WIN.get_width(), WIN.get_height()))
        clock.tick(60)

    # Quit pygame
    pygame.quit()
else:
    print(f'why tf is __name__ not "__main__" but instead "{__name__}"?!?!?!')
    input("Go on... seriously ! Thats not a rhetorical question. Why? --> ")
"""
import pygame
pygame.init()
screen = pygame.display.set_mode((640, 480))
clock = pygame.time.Clock()

def main():
   while True:
      for event in pygame.event.get():
            if event.type == pygame.QUIT:
               pygame.quit()
               return
            elif event.type == pygame.MOUSEWHEEL:
               print(event)
            else:
               print(event)
      clock.tick(60)

# Execute game:
main()"
"""