import pygame, sys, time

import control
import title_screen

print(str(time.time_ns()) + " Initialising main...")

# Initialize pygame
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
    WIN.fill((0, 0, 0))
    for e in pygame.event.get():
        if event.type == pygame.QUIT:
            done = True
            pygame.quit()
            print("Quitting...")
        control.update_input(e)

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

    title_screen.draw_menu_screen(WIN, control.GMCTRL, pygame)

    pygame.display.flip()

    clock.tick(60)
# Quit pygame
pygame.quit()
