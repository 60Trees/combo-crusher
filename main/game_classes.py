import pygame
import math
import collisions as COLLISIONS
import INP

left = 0
right = 1

previouslypausedgame = False
timer = 0

class Surfaces():
    def __init__(self):
        self.gui = pygame.surface.Surface((100, 100), pygame.SRCALPHA)
        self.characters = pygame.surface.Surface((100, 100), pygame.SRCALPHA)
        self.foreground = pygame.surface.Surface((100, 100), pygame.SRCALPHA)
        self.background = pygame.surface.Surface((100, 100), pygame.SRCALPHA)
surface = Surfaces()

class Camera():
    def __init__(self):
        self.pos = (0, 0)
        self.vel = (0, 0)
        self.zoom_in = 5
camera = Camera()

class Level():
    def __init__(self):
        self.FLOORS = [
            (
                (-100, -20),
                (100, 0)
            ),
            (
                (-200, 10),
                (-50, 20)
            ),
            (
                (-100, 40),
                (100, 20)
            )
        ]
        self.CEILINGS = [
            (
                (-60, -60),
                (100, -50)
            ),
        ]
        self.WALLS = [
            (
                (-60, -60),
                (100, -50)
            ),
        ]
lvl = Level()

class Player():
    def __init__(self):
        self.width = 15
        self.height = 23
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
    
    def isColliding(self, pos, type_of_collision):
        if type_of_collision == COLLISIONS.floorCol:
            x, y = pos
            isColliding = False
            for i in lvl.FLOORS:
                if COLLISIONS.iscolliding(i[0], i[1], (x, y), 16):
                    isColliding = True
            return isColliding
        elif type_of_collision == COLLISIONS.ceilCol:
            x, y = pos
            isColliding = False
            for i in lvl.CEILINGS:
                if COLLISIONS.iscolliding_ceiling(i[0], i[1], (x, y), 16):
                    isColliding = True
            return isColliding

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

        tmp2y += self.gravity

        tmpx += tmp2x
        tmpy += tmp2y

        if self.isColliding((tmpx, tmpy - self.height), COLLISIONS.ceilCol):
            while self.isColliding((tmpx, tmpy - self.height), COLLISIONS.floorCol):
                tmpy += 1
            tmp2y = max(0, tmp2y)
            self.isonground = True
        else:
            self.isonground = False

        if self.isColliding((tmpx, tmpy), COLLISIONS.floorCol):
            while self.isColliding((tmpx, tmpy), COLLISIONS.floorCol):
                tmpy -= 1
            tmp2y = min(0, tmp2y)
            self.isonground = True
        else:
            self.isonground = False

        self.pos = tmpx, tmpy
        self.vel = tmp2x, tmp2y

    def handle_anim(self):
        if self.actionstate == self.ACTION.idle:
            if self.ANIM.timer_max != 3:
                self.ANIM.timer = 0
                self.ANIM.timer_max = 3
            else:
                self.ANIM.timer += 1
                if self.ANIM.timer > self.ANIM.timer_max:
                    self.ANIM.timer = 0
            self.animstate = self.ANIM.idle[self.ANIM.timer]

        if self.actionstate == self.ACTION.walk:
            if self.ANIM.timer_max != 3:
                self.ANIM.timer = 0
                self.ANIM.timer_max = 3
            else:
                self.ANIM.timer += 1
                if self.ANIM.timer > self.ANIM.timer_max:
                    self.ANIM.timer = 0
            self.animstate = self.ANIM.walk[self.ANIM.timer]

        if not self.isonground:
            self.animstate = self.ANIM.fall
        if self.vel[1] < 0:
            self.animstate = self.ANIM.jump

    def get_current_state(self):
        return self.assets[self.animstate]

player = Player()