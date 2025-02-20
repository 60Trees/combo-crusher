import pygame, sys, time

import control
import game_main as GAME

print(str(time.time_ns()) + " Initialising main...")

# Initialise pygame
pygame.init()
pygame.font.init()

clock = pygame.time.Clock()

WIN = pygame.display.set_mode((200, 200), pygame.RESIZABLE)
pygame.display.set_caption("Push Fullscreen")

done = False

WIN.fill((0, 0, 255))
pygame.display.flip()

while not done:
    for event in pygame.event.get():
        if event.type == pygame.VIDEORESIZE:
            done = True

pygame.display.set_caption("Combo Crusher")

done = False

btnsPressed = ""

pygame.display.set_icon(pygame.image.load("main/assets/logo.png"))

# Main loop
while not done:
    WIN.fill((255, 255, 255))
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            done = True
            pygame.quit()
            print("Quitting...")
            sys.exit()
        else: control.update_input(event)

    tmp = ""
    tmp2 = 0
    for i in control.GMCTRL:
        tmp = tmp + ("▧ " if i else "▢ ")
        tmp2 += 1

    if tmp != btnsPressed:
        btnsPressed = tmp
        control.check_input()
        tmp = ""
        tmp2 = 0
        for i in control.GMCTRL:
            tmp = tmp + ("▧ " if i else "▢ ")
            tmp2 += 1
        print(btnsPressed + str(round(clock.get_fps())))
    print(GAME.title_screen.GUI.current_menu_screen)
    if "ingame" in GAME.title_screen.GUI.current_menu_screen:
        if GAME.draw_game(WIN, control.GMCTRL, not GAME.title_screen.GUI.current_menu_screen == "ingame"):
            if not "pausemenu" in GAME.title_screen.GUI.current_menu_screen: GAME.title_screen.GUI.current_menu_screen = "ingame/pausemenu"

    if GAME.title_screen.GUI.current_menu_screen in GAME.title_screen.GUI.menu_screen:
        if "ingame" in GAME.title_screen.GUI.current_menu_screen:
            pygame.draw.rect(
                pygame.surface.Surface((1, 1)),
                (50, 50, 50, 10),
                (0, 0, WIN.get_width(), WIN.get_height())
            )
        #print(f"Currently {title_screen.GUI.current_menu_screen} (: (: (: (:")
        GAME.title_screen.draw_menu_screen(WIN, control.GMCTRL, pygame)

    pygame.display.flip()

    clock.tick(60)
# Quit pygame
pygame.quit()