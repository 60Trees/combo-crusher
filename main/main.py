import pygame, sys, time

import controller
import title_screen

print(str(time.time_ns()) + " Initialising main...")

# Initialize pygame
pygame.init()

clock = pygame.time.Clock()

"""
pygame.joystick.init()


if pygame.joystick.get_count() == 0:
    print("No joystick detected")
else:
    # Use the first joystick
    joystick = pygame.joystick.Joystick(0)
    joystick.init()
    print(f"Controller {joystick.get_name()} detected!")
    joystick.rumble(1, 1, 500)

"""

WIN = pygame.display.set_mode((200, 200), pygame.RESIZABLE)
pygame.display.set_caption("Push Fullscreen")

done = False

while not done:
    for event in pygame.event.get():
        if event.type == pygame.VIDEORESIZE:
            done = True

pygame.display.set_caption("Smashy Smashy")

done = False

# Main loop
while not done:
    WIN.fill((0, 0, 0))
    for e in pygame.event.get():
        controller.update_input(event=e)
        if event.type == pygame.QUIT:
            done = True

    pygame.display.flip()

    clock.tick(60)
# Quit pygame
pygame.quit()