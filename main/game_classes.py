import math
import os

import input_ID as INP
import pygame
import util_handling

left = 0
right = 1

timer = 0

class Camera():
    def __init__(self):
        self.pos = (100, 100)
        self.vel = (0, 0)
        self.zoom_in = 3
        self.previousZoomIn = self.zoom_in
        self.topBorderHeight = 0
        self.bottomBorderHeight = 0
    def camera_transition(self, centerOn, speed):
        # The speed in seconds it takes to center camera
        posx, posy = centerOn
        camposx, camposy = self.pos

        camposx += (posx - camposx) / speed
        camposy += (posy - camposy) / speed

        centerOn = posx, posy
        self.pos = camposx, camposy
camera = Camera()

class Surface():
    def __init__(self):
        self.LEVEL = pygame.surface.Surface((1, 1))
surface = Surface()

class Level():
    def __init__(self):
        self.current_world = 1
        self.current_level = 1
        self.current_level_name = f"Level {self.current_world}-{self.current_level}"
        self.current_level_area = "Area1"

        class area_intGrids:
            Decor_underlay = []
            Interactable_tiles = []
            Regions = []
        self.current_area_intgrids = area_intGrids

        self.path_to_area = f"main/assets/game/levels/{self.current_level_name}/simplified/{self.current_level_area}"
        self.current_area_properties = util_handling.load(f"{self.path_to_area}/data.json")

        self.files = [f for f in os.listdir(self.path_to_area) if os.path.isfile(os.path.join(self.path_to_area, f))]
        for i in self.files:
            if i.endswith(".csv"):
                setattr(self.current_area_intgrids, i[:-4], util_handling.csv_to_array(f"{self.path_to_area}\{i}"))

    def draw_refresh(self, WIN):
        pass

    def draw(self, WIN):
        surface.LEVEL = pygame.surface.Surface(assets.current_area.get_size())

        # Blit level
        surface.LEVEL.blit(assets.current_area, (0, 0))

        # Blit player
        surf = assets.player_sprites[0]
        blittingPos = (
            player.pos[0] - player.width / 2,
            player.pos[1] - player.height,
        )

        surface.LEVEL.blit(
            pygame.transform.flip(
                surf,
                player.facing == left,
                False
            ),
            blittingPos
        )

        # Handle camera transitions
        camera.camera_transition(player.pos, speed = 5)

        try:
            current_zoomin_area = self.current_area_intgrids.Regions[math.floor((player.pos[1] - player.width / 2) / 16)][math.floor((player.pos[0] - player.height) / 16)]
            try:
                current_zoomin_area = int(current_zoomin_area)
            except ValueError:
                raise IndexError
            if current_zoomin_area > 0:
                camera.previousZoomIn = self.current_area_properties["customFields"][f"Zoom_in{current_zoomin_area}"]
        except IndexError:
            pass
        
        camera.zoom_in += (camera.previousZoomIn - camera.zoom_in) / 6

        self.current_area_properties["customFields"]["Zoom_in1"]

        WIN.blit(
            pygame.transform.scale(
                surface.LEVEL,
                (
                    surface.LEVEL.get_width() * camera.zoom_in,
                    surface.LEVEL.get_height() * camera.zoom_in
                )
            ),
            (
                -camera.pos[0] * camera.zoom_in + WIN.get_width() / 2,
                -camera.pos[1] * camera.zoom_in + WIN.get_height() / 2
            )
        )
lvl = Level()

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

class Assets():
    def __init__(self):
        self.player_sprites = [
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
        self.current_area = pygame.image.load(lvl.path_to_area + "/_composite.png")
assets = Assets()

class Player():
    def __init__(self):
        self.width = 15
        self.height = 23
        self.jumpheight = 7
        self.previous_isonground = True
        self.isonground = True
        self.gravity = 1
        self.gravityupdatetimer = 0
        self.animupdatetimer_maximum = 3

        self.ACTION = action_states()
        self.ANIM = anim_states()

        self.animupdatetimer = 0
        self.pos = (
            lvl.current_area_properties["entities"]["Player_Starting_position"][0]["x"],
            lvl.current_area_properties["entities"]["Player_Starting_position"][0]["y"]
        )
        self.vel = (0, 0)
        self.actionstate = 6
        self.previous_actionstate = self.actionstate
        self.animstate = 0
        self.facing = right
        self.hp = 100
        self.maxhp = 100
        self.walkingspeed = 1.1

    def handle_action(self, CTRL):
        tmpx, tmpy = self.pos
        if CTRL.pushed[INP.moveleft]:
            tmpx -= 3
        if CTRL.pushed[INP.moveright]:
            tmpx += 3
        if CTRL.pushed[INP.jump]:
            tmpy -= 3
        if CTRL.pushed[INP.sneak]:
            tmpy += 3
        self.pos = tmpx, tmpy

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
player = Player()