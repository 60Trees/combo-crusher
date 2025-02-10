import time, pygame, json_func

menu_title = pygame.image.load("main/assets/gui/title.png")
from control import INP

class action_states():
    walk = 0
    power_attack = 1
    swordfall = 2
    swordland = 3
    roll = 4
    dodge = 5

    idle = 6

    timer = 0
    timer_max = 0
ACTION = action_states()
class anim_states():
    fall = 0
    idle1 = 1
    idle2 = 2
    idle3 = 3
    idle4 = 4
    jump = 5
    land1 = 6
    land2 = 7
    swordfall = 8
    swordland = 9
    walk1 = 10
    walk2 = 11
    walk3 = 12
    walk4 = 13

    timer = 0
    timer_max = 0
ANIM = anim_states()

left = False
right = True

class class_GAME():
    def __init__(self):
        self.hi = 3
        class Surfaces():
            def __init__(self):
                self.gui = pygame.surface.Surface((100, 100))
                self.characters = pygame.surface.Surface((100, 100))
                self.foreground = pygame.surface.Surface((100, 100))
                self.background = pygame.surface.Surface((100, 100))
        self.surface = Surfaces()

        class Assets():
            def __init__(self):
                self.player [
                    pygame.image.load("main/assets/game/player/fall.png"),
                    pygame.image.load("main/assets/game/player/idle1.png"),
                    pygame.image.load("main/assets/game/player/idle2.png"),
                    pygame.image.load("main/assets/game/player/idle3.png"),
                    pygame.image.load("main/assets/game/player/idle4.png"),
                    pygame.image.load("main/assets/game/player/jump.png"),
                    pygame.image.load("main/assets/game/player/land1.png"),
                    pygame.image.load("main/assets/game/player/land2.png"),
                    pygame.image.load("main/assets/game/player/swordfall.png"),
                    pygame.image.load("main/assets/game/player/swordland.png"),
                    pygame.image.load("main/assets/game/player/walk1.png"),
                    pygame.image.load("main/assets/game/player/walk2.png"),
                    pygame.image.load("main/assets/game/player/walk3.png"),
                    pygame.image.load("main/assets/game/player/walk4.png")
                ]

        class Player():
            def __init__(self):
                self.pos = (0, 0)
                self.vel = (0, 0)
                self.actionstate = 1
                self.facing = right
                self.hp = 100
                self.maxhp = 100
            def handle_anim(self):
                if self.actionstate == ACTION.idle:
                    if ANIM.timer_max != 3:
                        ANIM.timer = 0
                        ANIM.timer_max = 3
                    else:
                        ANIM.timer += 1
                        if ANIM.timer > ANIM.timer_max:
                            ANIM.timer = 0
                if self.actionstate == ACTION.walk:
                    if ANIM.timer_max != 3:
                        ANIM.timer = 0
                        ANIM.timer_max = 3
                    else:
                        ANIM.timer += 1
                        if ANIM.timer > ANIM.timer_max:
                            ANIM.timer = 0

        self.player = Player()
GAME = class_GAME()

print(str(time.time_ns()) + " Initialising title_screen.py")

def draw_game(WIN, controls, pyg):
    pass
    #print(GUI.controls_previously_pressed)

print(str(time.time_ns()) + " Done")