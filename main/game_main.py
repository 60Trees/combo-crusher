import time, pygame, json_func, math

import title_screen
import INP

menu_title = pygame.image.load("main/assets/gui/title.png")


left = False
right = True

class class_GAME():
    def __init__(self):
        
        self.timer = 0

        class Surfaces():
            def __init__(self):
                self.gui = pygame.surface.Surface((100, 100), pygame.SRCALPHA)
                self.characters = pygame.surface.Surface((100, 100), pygame.SRCALPHA)
                self.foreground = pygame.surface.Surface((100, 100), pygame.SRCALPHA)
                self.background = pygame.surface.Surface((100, 100), pygame.SRCALPHA)
        self.surface = Surfaces()

        class Camera():
            def __init__(self):
                self.pos = (0, 0)
                self.vel = (0, 0)
                self.zoom_in = 5
        self.camera = Camera()

        class Level():
            def __init__(self):
                self.collisions_floor = [
                    (
                        (-55, 0),
                        (55, 0)
                    )
                ]
        self.lvl = Surfaces()

        class Player():
            def __init__(self):
                self.jumpheight = 10
                self.previous_isonground = True
                self.isonground = True
                self.gravity = 1
                self.gravitycounter = 4
                self.gravitycounter_maximum = 4
                self.animupdatetimer_maximum = 15
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
                self.ACTION = action_states()

                class anim_states():
                    fall = 0
                    idle = [1, 2, 3, 4]
                    idle_anim_speed = 0.75
                    idle1 = 1
                    idle2 = 2
                    idle3 = 3
                    idle4 = 4
                    jump = 5
                    land = [6, 7]
                    land1 = 6
                    land2 = 7
                    swordfall = 8
                    swordland = 9
                    walk = [10, 11, 12, 13]
                    walk_anim_speed = 1.5
                    walk1 = 10
                    walk2 = 11
                    walk3 = 12
                    walk4 = 13

                    timer = 0
                    timer_max = 0
                self.ANIM = anim_states()


                class Assets():
                    def __init__(self):
                        self.sprites = [
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
                self.animupdatetimer = 0
                self.assets = Assets()
                self.pos = (0, 0)
                self.vel = (0, 0)
                self.actionstate = 6
                self.previous_actionstate = self.actionstate
                self.animstate = 0
                self.facing = right
                self.hp = 100
                self.maxhp = 100
                self.walkingspeed = 1.25
            def handle_action(self, CTRL):
                if self.actionstate == self.ACTION.idle or self.actionstate == self.ACTION.walk:
                    tmpx, tmpy = self.vel
                    if CTRL[INP.moveleft] and not CTRL[INP.moveright]:
                        tmpx -= self.walkingspeed
                        self.facing = left
                        self.actionstate = self.ACTION.walk
                    elif CTRL[INP.moveright] and not CTRL[INP.moveleft]:
                        tmpx += self.walkingspeed
                        self.facing = right
                        self.actionstate = self.ACTION.walk
                    else:
                        self.actionstate = self.ACTION.idle
                    #print(f"Before Player vel={(tmpx, tmpy)}")
                    if tmpx != 0:
                        tmpx /= 1.05
                        tmpx = (math.floor(tmpx) if self.vel[0] > 0 else math.ceil(tmpx))
                    #print(f"After Player vel={(tmpx, tmpy)}")

                    if self.isonground and CTRL[INP.jump]:
                        self.isonground = False
                        tmpy -= self.jumpheight

                    self.vel = tmpx, tmpy
                if self.previous_actionstate != self.actionstate or self.previous_isonground != self.isonground:
                    self.animupdatetimer = self.animupdatetimer_maximum + 1
                    self.previous_isonground = self.isonground
                    self.previous_actionstate = self.actionstate

                tmpx, tmpy = self.pos
                tmp2x, tmp2y = self.vel

                tmpx += tmp2x
                tmpy += tmp2y

                tmp2y += self.gravity

                if tmpy >= 0:
                    tmpy = 0
                    tmp2y = min(0, tmp2y)
                    self.isonground = True
                else: self.isonground = False

                self.pos = tmpx, tmpy
                self.vel = tmp2x, tmp2y
                #print(f"Player pos={self.pos}, player vel={self.vel}")

            def handle_anim(self):
                if self.actionstate == self.ACTION.idle:
                    #print(f"Hi, {self.ANIM.timer_max}, {self.ANIM.timer}")
                    if self.ANIM.timer_max != 3:
                        self.ANIM.timer = 0
                        self.ANIM.timer_max = 3
                    else:
                        self.ANIM.timer += 1
                        if self.ANIM.timer > self.ANIM.timer_max:
                            self.ANIM.timer = 0
                    self.animstate = self.ANIM.idle[self.ANIM.timer]
                if self.actionstate == self.ACTION.walk:
                    #print("Bye")
                    if self.ANIM.timer_max != 3:
                        self.ANIM.timer = 0
                        self.ANIM.timer_max = 3
                    else:
                        self.ANIM.timer += 1
                        if self.ANIM.timer > self.ANIM.timer_max:
                            self.ANIM.timer = 0
                    self.animstate = self.ANIM.walk[self.ANIM.timer]
                if not self.isonground: self.animstate = self.ANIM.fall
                if self.vel[1] < 0: self.animstate = self.ANIM.jump
                if self.vel[1] > 0: print("Falling...")

            def get_current_state(self):
                return self.assets[self.animstate]

        self.player = Player()
GAME = class_GAME()

print(str(time.time_ns()) + " Initialising title_screen.py")

def draw_game(WIN, CTRL, pyg):
    GAME.surface.characters = pygame.surface.Surface(WIN.get_size())
    GAME.surface.background.fill((255, 0, 0, 255))
    
    GAME.camera.pos = (WIN.get_width() / 2 / GAME.camera.zoom_in, WIN.get_height() / 2 / GAME.camera.zoom_in)

    if GAME.timer == 0:
        GAME.player.pos = (0, 0)
        GAME.gui = pygame.surface.Surface(WIN.get_size(), pygame.SRCALPHA)
        GAME.surface.characters = pygame.surface.Surface(WIN.get_size(), pygame.SRCALPHA)
        GAME.surface.foreground = pygame.surface.Surface(WIN.get_size(), pygame.SRCALPHA)
        GAME.surface.background = pygame.surface.Surface(WIN.get_size(), pygame.SRCALPHA)
        GAME.surface.gui.fill((0, 0, 0, 0))
        GAME.surface.characters.fill((0, 0, 0, 0))
        GAME.gui.fill((0, 0, 0, 0))
        GAME.gui.fill((0, 0, 0, 0))
    GAME.timer += 1

    surf = GAME.player.assets.sprites[GAME.player.animstate]
    GAME.surface.characters.blit(
        pygame.transform.scale(
            pygame.transform.flip(
                surf,
                GAME.player.facing == left,
                False
            ),
            (surf.get_width() * GAME.camera.zoom_in, surf.get_height() * GAME.camera.zoom_in)
        ),
        (
            round(GAME.player.pos[0]) * GAME.camera.zoom_in + GAME.camera.pos[0] * GAME.camera.zoom_in,
            round(GAME.player.pos[1]) * GAME.camera.zoom_in + GAME.camera.pos[1] * GAME.camera.zoom_in
        )
    )
    pygame.draw.rect(
        WIN,
        (100, 100, 100),
        (
            0,
            WIN.get_height() / 2,
            WIN.get_width(),
            WIN.get_height()
        )
    )
    #print(f"Printing player at X={GAME.player.pos[0] * GAME.camera.zoom_in + GAME.camera.pos[0] * GAME.camera.zoom_in}, Y={GAME.player.pos[1] * GAME.camera.zoom_in + GAME.camera.pos[1] * GAME.camera.zoom_in}")

    GAME.player.animupdatetimer += 1
    print(f"Before: Player pos={GAME.player.pos},vel={GAME.player.vel},isOnGr={GAME.player.isonground},actionstate={GAME.player.actionstate}")
    GAME.player.handle_action(CTRL)
    print(f"After:  Player pos={GAME.player.pos},vel={GAME.player.vel},isOnGr={GAME.player.isonground},actionstate={GAME.player.actionstate}")
    if GAME.player.animupdatetimer > GAME.player.animupdatetimer_maximum:
        GAME.player.handle_anim()
        tmp = "right" if GAME.player.facing else "left"
        print(f"Updating anim, animstate={GAME.player.animstate}, facing={tmp}, actionstate={GAME.player.actionstate}")
        GAME.player.animupdatetimer = 0

    WIN.blit(GAME.surface.background, (0, 0))
    WIN.blit(GAME.surface.characters, (0, 0))
    WIN.blit(GAME.surface.foreground, (0, 0))
    WIN.blit(GAME.surface.gui, (0, 0))

print(str(time.time_ns()) + " Done")