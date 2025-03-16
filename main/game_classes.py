import math
from typing import List, Tuple

import BlazeSudio.Game.world as LDTK
import input_ID as INP
import pygame
import title_screen_layout
from control import Active_controls

left = False
right = True

class LevelError(Exception):
    def __init__(self, message):
        super().__init__(message)
        self.message = message
class EntityError(Exception):
    def __init__(self, message):
        super().__init__(message)
        self.message = message
class EntityTypeError(Exception):
    def __init__(self, message):
        super().__init__(message)
        self.message = message

class Game:
    def __init__(self, WIN: pygame.Surface):
        self.WIN: pygame.Surface = WIN
        self.WORLD = World_map(self)
        self.LEVEL = Level(self)
        self.PLAYER = Player(self)
        self.CAMERA = Camera(self)
        self.SURFACE = pygame.Surface((1, 1))
        self.GUI: class_GUI = class_GUI()
        self.ASSETS = Assets(self)
        self.ISPAUSED = True
        self.GMCTRL: Active_controls = None

pygame.font.init()

class class_GUI():
    def __init__(self):
        self.layout = title_screen_layout.Layout()

        self.timer = 0
        self.timer_maximum = 15
        self.current_menu_screen = self.layout.startup
        self.menu_screen = self.layout.layout
        self.selected_button = 0
        self.selected_button_maximum = self.menu_screen[self.current_menu_screen]["max_buttons"]
        self.anim = [
            3.000, 3.000, 3.000
        ]
        self.scale = 5

        self.assets = class_GUI_Assets(self)
        self.time_passed = 0
    def reset_anim(self, WIN):
        print("Resetting anim!!")
        self.anim[0] = 3.000
        self.anim[1] = 3.000
        self.anim[2] = 3.000
        self.time_passed  = 0
    def draw_menu_screen(self, game: Game):
        self.time_passed += 1
        
        if game.GMCTRL.tapped[INP.GUI_Up]:
            if self.selected_button is not None:
                self.selected_button -= 1
            else:
                self.selected_button = 0

        if game.GMCTRL.tapped[INP.GUI_Down]:
            if self.selected_button is not None:
                self.selected_button += 1
            else:
                self.selected_button = 0

        if game.GMCTRL.tapped[INP.GUI_Left] or game.GMCTRL.tapped[INP.item_left]:
            if self.selected_button is not None:
                self.selected_button -= 2
            else:
                self.selected_button = 0

        if game.GMCTRL.tapped[INP.GUI_Right] or game.GMCTRL.tapped[INP.item_right]:
            if self.selected_button is not None:
                self.selected_button += 2
            else:
                self.selected_button = 0
        
            while self.selected_button > self.selected_button_maximum:
                self.selected_button -= self.selected_button_maximum + 1
            while self.selected_button < 0:
                self.selected_button += self.selected_button_maximum + 1

        future_menu_screen = None

        timer_goesup = False

        if game.GMCTRL.cursor.hasMoved:
            self.selected_button = None

        for i in range(len(self.menu_screen[self.current_menu_screen]["buttons"])):
            current_button = self.menu_screen[self.current_menu_screen]["buttons"][i]
            
            # This is where the button will be drawn
            button_positionX = game.WIN.get_width() / 2 -  (self.scale + (self.assets.menu_buttons[0].get_width() * self.scale)  * self.menu_screen[self.current_menu_screen]["starting_point"][0]) / 2 + (self.scale + self.assets.menu_buttons[0].get_width() * self.scale) * current_button["pos_multiplier"][0]
            button_positionX += (self.anim[current_button["anim"]] * (game.WIN.get_width() if current_button["anim_positive"] else -game.WIN.get_width()))

            button_positionY = game.WIN.get_height() / 2 - (self.scale + (self.assets.menu_buttons[0].get_height() * self.scale) * self.menu_screen[self.current_menu_screen]["starting_point"][1]) / 2 + (self.scale + self.assets.menu_buttons[0].get_height() * self.scale) * current_button["pos_multiplier"][1]
            if current_button["button_assignment"] is not None and pygame.Rect(button_positionX, button_positionY, self.assets.menu_buttons[0].get_width() * self.scale, self.assets.menu_buttons[0].get_height() * self.scale).collidepoint(game.GMCTRL.cursor.pos):
                self.selected_button = current_button["button_assignment"]

            tmp_ispushed = \
                (game.GMCTRL.pushed[current_button["button_push"]] or (game.GMCTRL.cursor.click.hold[0] and self.selected_button == current_button["button_assignment"])) \
                    if current_button["button_push"] is not None else \
                ((game.GMCTRL.pushed[INP.GUI_A] or game.GMCTRL.cursor.click.hold[0]) and self.selected_button == current_button["button_assignment"])

            if current_button["button_assignment"] is None:
                tmp_ispushed = False

            if False if current_button["button_push"] is None else game.GMCTRL.pushed[current_button["button_push"]]:
                self.selected_button = current_button["button_assignment"]
            if tmp_ispushed:
                timer_goesup = True
                if self.timer >= self.timer_maximum:
                    future_menu_screen = current_button["button_push_menu_screen"]
                    self.timer = 0
            
            tmp_imgs: pygame.Surface = None
            if current_button["image_push"] is not None and current_button["image_hover"] is not None:
                if current_button["image"] is not None:
                    tmp_imgs = (eval(current_button["image_push"]) if tmp_ispushed else (eval(current_button["image_hover"]) if self.selected_button == current_button["button_assignment"] else eval(current_button["image"])))
                    tmp_imgs = pygame.transform.scale(tmp_imgs, (tmp_imgs.get_width() * self.scale, tmp_imgs.get_height() * self.scale))
            elif current_button["image"] is not None:
                tmp_imgs = eval(current_button["image"])
                tmp_imgs = pygame.transform.scale(tmp_imgs, (tmp_imgs.get_width() * self.scale, tmp_imgs.get_height() * self.scale))
                game.GUI.assets.title_logo
            if tmp_imgs is not None:
                game.WIN.blit(tmp_imgs, (
                    button_positionX,
                    button_positionY
                ))

            # Draws the text on the button (if it has text)
            if current_button["text"] is not None:
                tmp_fontsurf = self.assets.pixelfont.render(current_button["text"][0], current_button["text"][1], current_button["text"][2])
                tmp_fontsurf = pygame.transform.scale(tmp_fontsurf, (
                    (tmp_fontsurf.get_width() / tmp_fontsurf.get_height()) * (self.scale * 8),
                    self.scale * 8
                ))
                game.WIN.blit(tmp_fontsurf, (
                    button_positionX + self.assets.menu_buttons[0].get_width() * self.scale / 2 - tmp_fontsurf.get_width() / 2,
                    button_positionY + 4 * self.scale + (self.scale * 2 if tmp_ispushed else 0)
                ))

        if future_menu_screen is not None:
            self.current_menu_screen = future_menu_screen
            if self.current_menu_screen in self.menu_screen:
                self.selected_button_maximum = self.menu_screen[self.current_menu_screen]["max_buttons"]

        if timer_goesup:
            self.timer += 1
        else:
            self.timer /= 1.1
            self.timer -= 1

        self.timer = max(0, min(self.timer, self.timer_maximum))

        if game.WIN.get_width() * self.anim[0] > 1:
            self.anim[0] /= 1.05
        else:
            self.anim[0] = 0

        if self.time_passed > 20:
            if game.WIN.get_width() * self.anim[1] > 1:
                self.anim[1] /= 1.05
            else:
                self.anim[1] = 0
        if self.time_passed > 40:
            if game.WIN.get_width() * self.anim[2] > 1:
                self.anim[2] /= 1.05
            else:
                self.anim[2] = 0

        if self.current_menu_screen in self.menu_screen:
            pygame.draw.rect(game.WIN, (0, 255, 0), pygame.Rect(
                0,
                game.WIN.get_height() - self.scale,
                game.WIN.get_width() / self.timer_maximum * self.timer,
                self.scale
            ))

class class_GUI_Assets():
    def __init__(self, classgui: class_GUI):
        self.pixelfont = pygame.font.Font('main/assets/font.ttf', 36)
        self.menu_buttons = [
            pygame.image.load("main/assets/gui/button_a_default.png"),
            pygame.image.load("main/assets/gui/button_b_default.png"),
            pygame.image.load("main/assets/gui/button_x_default.png"),
            pygame.image.load("main/assets/gui/button_y_default.png"),
            pygame.image.load("main/assets/gui/button_normal_default.png"),
        ]

        self.menu_buttons_selected = [
            pygame.image.load("main/assets/gui/button_a_hover.png"),
            pygame.image.load("main/assets/gui/button_b_hover.png"),
            pygame.image.load("main/assets/gui/button_x_hover.png"),
            pygame.image.load("main/assets/gui/button_y_hover.png"),
            pygame.image.load("main/assets/gui/button_normal_hover.png"),
        ]

        self.menu_buttons_push = [
            pygame.image.load("main/assets/gui/button_a_push.png"),
            pygame.image.load("main/assets/gui/button_b_push.png"),
            pygame.image.load("main/assets/gui/button_x_push.png"),
            pygame.image.load("main/assets/gui/button_y_push.png"),
            pygame.image.load("main/assets/gui/button_normal_push.png"),
        ]

        self.title_logo = pygame.transform.scale(
            pygame.image.load("main/assets/gui/title.png"), (
                self.menu_buttons[0].get_width() * 2 + classgui.scale,
                self.menu_buttons[0].get_height() * 2 + classgui.scale
            )
        )

class Camera():
    def __init__(self, game: Game):
        self.pos = (100, 100)
        self.vel = (0, 0)
        self.zoom_in = 3
        self.previousZoomIn = self.zoom_in
        self.topBorderHeight = 0
        self.bottomBorderHeight = 0
    def camera_transition(self, game: Game, centerOn, speed):
        # The speed in seconds it takes to center camera
        posx, posy = centerOn
        if game.LEVEL.LVL_cameraBounds is not None:
            print(f"Camera bounds: {game.LEVEL.LVL_cameraBounds.rectangle}, Window left edge: {posx - game.WIN.get_width() / 2 / self.zoom_in}, Window right edge: {posx + game.WIN.get_width() / 2 / self.zoom_in}")
        if posx - game.WIN.get_width() / 2 / self.zoom_in < game.LEVEL.LVL_cameraBounds.rectangle.left:
            posx = game.LEVEL.LVL_cameraBounds.rectangle.left + game.WIN.get_width() / 2 / self.zoom_in
        if posx + game.WIN.get_width() / 2 / self.zoom_in > game.LEVEL.LVL_cameraBounds.rectangle.right:
            posx = game.LEVEL.LVL_cameraBounds.rectangle.right - game.WIN.get_width() / 2 / self.zoom_in
        if posy - game.WIN.get_height() / 2 / self.zoom_in < game.LEVEL.LVL_cameraBounds.rectangle.top:
            posy = game.LEVEL.LVL_cameraBounds.rectangle.top + game.WIN.get_height() / 2 / self.zoom_in
        if posy + game.WIN.get_height() / 2 / self.zoom_in > game.LEVEL.LVL_cameraBounds.rectangle.bottom:
            posy = game.LEVEL.LVL_cameraBounds.rectangle.bottom - game.WIN.get_height() / 2 / self.zoom_in
        camposx, camposy = self.pos

        camposx += (posx - camposx) / speed
        camposy += (posy - camposy) / speed

        if camposx - game.WIN.get_width() / 2 / self.zoom_in < game.LEVEL.LVL_cameraBounds.rectangle.left:
            camposx = game.LEVEL.LVL_cameraBounds.rectangle.left + game.WIN.get_width() / 2 / self.zoom_in
        if camposx + game.WIN.get_width() / 2 / self.zoom_in > game.LEVEL.LVL_cameraBounds.rectangle.right:
            camposx = game.LEVEL.LVL_cameraBounds.rectangle.right - game.WIN.get_width() / 2 / self.zoom_in
        if camposy - game.WIN.get_height() / 2 / self.zoom_in < game.LEVEL.LVL_cameraBounds.rectangle.top:
            camposy = game.LEVEL.LVL_cameraBounds.rectangle.top + game.WIN.get_height() / 2 / self.zoom_in
        if camposy + game.WIN.get_height() / 2 / self.zoom_in > game.LEVEL.LVL_cameraBounds.rectangle.bottom:
            camposy = game.LEVEL.LVL_cameraBounds.rectangle.bottom - game.WIN.get_height() / 2 / self.zoom_in
        self.pos = camposx, camposy

class Surface():
    def __init__(self):
        self.LEVEL = pygame.surface.Surface((1, 1))

class World_map():
    def __init__(self, game: Game):
        self.CURWORLD = 1
        self.CURLEVEL = 1
        self.CURAREA = 1
    def get_level_name(self):
        return f"Level {self.CURWORLD}-{self.CURLEVEL}"

class Region():
    def __init__(self, entity: LDTK.ldtk.Entity, entityDefs: dict):
        """
        This is a region class that turns an entity into a region. If the entity doesn't have the tag`"Region"`in it, then it raises an`EntityTypeError`, so it's reccomended to wrap it in a`try`loop.

        Args:
            entity (LDTK.ldtk.Entity): The entity to turn into a region
            entityDefs (dict): This is the defs located in ldtk
        ## Usage:

        Define a region by doing:
        ```
        region = Region()
        ```

        ```
        region.isColliding(position: pygame.Rect) -> bool
        ```
        >This lets you input a pygame Rectangle and outputs whether or not the rectangle is colliding with the region or not.

        ```
        region.type: str
        ```
        >This is the type of the region. There are multiple different types, for example `Camera_zoomin` and maybe `outOfBounds`

        """
        self.type: str = None
        self.define_type(entity, entityDefs)
        self.entity: LDTK.ldtk.Entity = entity

        class RegionTypes:
            def __init__(self):
                self.camera: str = "Camera_zoomin"
                self.cameraBounds: str = "Camera_bounds"
        self.types = RegionTypes()

        if self.type == self.types.camera:
            self.camera_init()

        self.rectangle = pygame.rect.Rect(
            self.entity.ScaledPos[0],
            self.entity.ScaledPos[1],
            self.entity.width,
            self.entity.height
        )

    def camera_init(self):
        self.camera_zoomin_level: float = None

        for i in self.entity.fieldInstances:
            if i["__identifier"] == "Camera_zoomin_level":
                if i["__type"] == "Float":
                    self.camera_zoomin_level = i["__value"]
                else:
                    raise TypeError(f"Camera_zoomin_level is a {i["__type"]} instead of expexted type Float")
        
        if self.camera_zoomin_level is None:
            raise AttributeError(f"No attribute Camera_zoomin_level in {self.entity.fieldInstances}")

    def define_type(self, entity: LDTK.ldtk.Entity, entityDefs: dict):
        temp_entitylist = []
        for i in entityDefs:
            temp_entitylist.append(i["identifier"])
            if i["identifier"] == entity.identifier:
                if "Region" in i["tags"]:
                    self.type = entity.identifier
                else:
                    raise EntityTypeError(f"Entity of type ({entity.identifier}) with tags {i["tags"]} is not Region")
        
        if self.type is None:
            EntityError(f"Entity of type ({entity.identifier}) does not exist in defs ({temp_entitylist})")

        del temp_entitylist
    
    def isColliding(self, position: pygame.rect.Rect) -> bool:
        return self.rectangle.colliderect(position)

class Level_Interactables():
    def __init__(self, game: Game):
        self.solid: List[List[int]] = None
        self.nonsolid: List[List[int]] = None

class Level():
    def __init__(self, game: Game):
        self.current_map = LDTK.World(f"main/assets/game/levels/{game.WORLD.get_level_name()}.ldtk")
    
        self.LVL = self.current_map.get_level(0)
        self.LVL_img = self.current_map.get_pygame(0)

        self.LVL_INTS = Level_Interactables(game)
        for i in self.LVL.layers:
            
            print(f"Layer {i.identifier} with intgrid {i.intgrid.intgrid}")
            if i.identifier == "Solid":
                self.LVL_INTS.solid = i.intgrid.intgrid
            if i.identifier == "Nonsolid":
                self.LVL_INTS.nonsolid = i.intgrid.intgrid

        self.player_start = None

        self.LVL_regions: List[Region] = []

        self.LVL_cameraBounds: Region = None

        for i in self.LVL.entities:
            if i.identifier == "Player_starting_pos":
                self.player_start = i.ScaledPos
            else:
                try:
                    self.LVL_regions.append(Region(i, self.LVL.defs["entities"]))
                    if self.LVL_regions[-1].type == self.LVL_regions[-1].types.cameraBounds:
                        self.LVL_cameraBounds = self.LVL_regions[-1]
                except EntityTypeError:
                    pass
            print(f"Entity {i.identifier} with scaled pos {i.ScaledPos} and unscaled pos {i.UnscaledPos}, DefUID: {i.defUid}")
        print(f"Regions: {self.LVL_regions}")

        if self.player_start is None:
            raise LevelError("Current level has no player start in it! You need to add a player start entity inside the level")

    def render(self) -> Surface:
        if self.LVL_img is None:
            self.LVL_img = self.current_map.get_pygame()
        return self.LVL_img

    def draw_refresh(self, game: Game):
        pass

    def draw(self, game: Game):
        game.SURFACE = pygame.surface.Surface(self.LVL_img.get_size())

        # Blit level
        game.SURFACE.blit(self.LVL_img, (0, 0))

        # Blit player
        surf = game.ASSETS.player_sprites[0]
        blittingPos = (
            game.PLAYER.pos[0] - game.PLAYER.width / 2,
            game.PLAYER.pos[1] - game.PLAYER.height,
        )

        game.SURFACE.blit(
            pygame.transform.flip(
                surf,
                game.PLAYER.facing == left,
                False
            ),
            blittingPos
        )

        pygame.draw.rect(game.SURFACE, (255, 0, 0), game.PLAYER.get_rect(), 1)

        # Handle camera transitions
        game.CAMERA.camera_transition(game, game.PLAYER.pos, speed = 5)

        current_zoomin_area = 0
        
        for REGION in self.LVL_regions:
            if REGION.isColliding(game.PLAYER.get_rect()) and REGION.type == REGION.types.camera:
                current_zoomin_area = REGION.camera_zoomin_level
        if current_zoomin_area > 0:
            game.CAMERA.previousZoomIn = current_zoomin_area
        
        game.CAMERA.zoom_in += (game.CAMERA.previousZoomIn - game.CAMERA.zoom_in) / 6

        """
        blittingPos = (
            -game.CAMERA.pos[0] * game.CAMERA.zoom_in + game.WIN.get_width() / 2,
            -game.CAMERA.pos[1] * game.CAMERA.zoom_in + game.WIN.get_height() / 2
        )
        game.WIN.blit(
            pygame.transform.scale(
                game.SURFACE,
                (
                    game.SURFACE.get_width() * game.CAMERA.zoom_in,
                    game.SURFACE.get_height() * game.CAMERA.zoom_in
                )
            ), blittingPos
        )
        """
        
        cropping_area = [
            math.floor(game.CAMERA.pos[0] - (game.WIN.get_width() / (2 * game.CAMERA.zoom_in))),
            math.floor(game.CAMERA.pos[1] - (game.WIN.get_height() / (2 * game.CAMERA.zoom_in))),
            math.ceil(game.WIN.get_width() / game.CAMERA.zoom_in) + 1,
            math.ceil(game.WIN.get_height() / game.CAMERA.zoom_in) + 1
        ]

        visible_rect = pygame.Rect(
            max(game.SURFACE.get_rect().x, cropping_area[0]),
            max(game.SURFACE.get_rect().y, cropping_area[1]),
            min(cropping_area[2], game.SURFACE.get_rect().width - max(game.SURFACE.get_rect().x, cropping_area[0])),
            min(cropping_area[3], game.SURFACE.get_rect().height - max(game.SURFACE.get_rect().y, cropping_area[1]))
        )

        # Crop the visible region with adjusted boundaries
        cropped = game.SURFACE.subsurface(visible_rect)

        scaled_width = max(1, round(visible_rect.width * game.CAMERA.zoom_in))
        scaled_height = max(1, round(visible_rect.height * game.CAMERA.zoom_in))

        scaled = pygame.transform.scale(cropped, (scaled_width, scaled_height))

        blittingPos = (
            round((game.WIN.get_width() / 2) - (game.CAMERA.pos[0] - visible_rect.left) * game.CAMERA.zoom_in),
            round((game.WIN.get_height() / 2) - (game.CAMERA.pos[1] - visible_rect.top) * game.CAMERA.zoom_in)
        )

        # Blit the scaled surface to the screen
        game.WIN.blit(scaled, blittingPos)
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
    def __init__(self, game: Game):
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
        
        self.current_area: pygame.Surface = None
    def update_current_area(self, game: Game):

        self.current_area = game.LEVEL.draw(game)

class Player():
    def __init__(self, game: Game):
        self.width = 15
        self.height = 23
        self.jumpheight = 10

        # Deaccelerates horizontally (by dividing itself by the value)
        self.horizontal_movement_deacceleration = 1.5

        # Deaccelerates vertically (by dividing itself by the value)
        self.vertical_movement_deacceleration = 1.5

        self.vertical_movement_max_speed = 3
        self.vertical_movement_min_speed = -self.jumpheight

        self.isonground = True
        self.gravity = 0.5

        self.ACTION = action_states()
        self.ANIM = anim_states()

        self.collision_bottom = 0

        self.animupdatetimer = 0
        self.pos = game.LEVEL.player_start
        self.previous_pos = game.LEVEL.player_start
        self.vel = (0, 0)
        self.actionstate = 6
        self.previous_actionstate = self.actionstate
        self.animstate = 0
        self.facing = right
        self.hp = 100
        self.maxhp = 100
        
        # 1 pixel per tick per tick (60 pixels per second per second)
        self.walkingspeed = 1

    def pos_to_rect(self, pos: Tuple[float, float]) -> pygame.Rect:
        return pygame.rect.Rect(
            pos[0] - self.width / 2,
            pos[1] - self.height,
            self.width,
            self.height
        )

    def get_rect(self) -> pygame.Rect:
        return pygame.rect.Rect(
            self.pos[0] - self.width / 2,
            self.pos[1] - self.height,
            self.width,
            self.height
        )

    def collision_intgrid(self, intgrid: List[List[int]], pos: Tuple[int, int], collision_block_side: str = "any") -> int:
        if collision_block_side == "any":
            return intgrid[pos[0]][pos[1]]
        elif collision_block_side == "u":
            return 0 if intgrid[pos[0] + 1][pos[1]] else intgrid[pos[0]][pos[1]]
        elif collision_block_side == "d":
            return 0 if intgrid[pos[0] - 1][pos[1]] else intgrid[pos[0]][pos[1]]
        elif collision_block_side == "l":
            return 0 if intgrid[pos[0]][pos[1] + 1] else intgrid[pos[0]][pos[1]]
        elif collision_block_side == "r":
            return 0 if intgrid[pos[0]][pos[1] - 1] else intgrid[pos[0]][pos[1]]
        else:
            raise NameError(f'Collision block side "{collision_block_side}" does not match up with "any", "u", "d", "l" or "r".')

    def check_collisions(self, game: Game, intgrid: List[List[int]], player: pygame.Rect, previus_player: pygame.Rect, collision_side: str = "d", collision_block_side: str = "any") -> int:
        """
        Inputs the intgrid and the side of the collision, outputs the tile it's colliding with.

        `collision_side` can only be`"u"`for up,`"d"`for down,`"l"`for left and`"r"`for right. Otherwise it will raise a NameError

        Args:
            game (Game): _description_
            intgrid (List[List[int]]): _description_
            player (pygame.Rect): The player rectagle to test collisions on.
            collision_side (str, optional): _description_. Defaults to "d".

        Raises:
            NameError: If the collision direction string does not match with`"u"`for up,`"d"`for down,`"l"`for left or`"r"`for right, then it raises a NameError.

        Returns:
            int: This is the intgrid tile that the character is colliding with on the`collision_side`side of the hitbox. Please note that it will return -1 if it's out of bounds.
        """
        collisionInt = 0
        if collision_side.lower() == "u":
            try:

                playerPos = (math.floor((player.y) / 16), math.floor((player.x + player.width / 2) / 16))
                collisionInt = self.collision_intgrid(intgrid, playerPos, collision_block_side)

                if collisionInt == 0:
                    playerPos = (math.floor((player.y) / 16), math.floor((player.x) / 16))
                    collisionInt = self.collision_intgrid(intgrid, playerPos, collision_block_side)
                if collisionInt == 0:
                    playerPos = (math.floor((player.y) / 16), math.floor((player.x + player.width) / 16))
                    collisionInt = self.collision_intgrid(intgrid, playerPos, collision_block_side)
            except IndexError:
                collisionInt = -1

        elif collision_side.lower() == "d":
            try:
                playerPos = (math.floor((player.y + player.height) / 16), math.floor((player.x + player.width / 2) / 16))
                collisionInt = self.collision_intgrid(intgrid, playerPos, collision_block_side)

                if collisionInt == 0:
                    playerPos = (math.floor((player.y + player.height) / 16), math.floor((player.x) / 16))
                    collisionInt = self.collision_intgrid(intgrid, playerPos, collision_block_side)
                if collisionInt == 0:
                    playerPos = (math.floor((player.y + player.height) / 16), math.floor((player.x + player.width) / 16))
                    collisionInt = self.collision_intgrid(intgrid, playerPos, collision_block_side)
            except IndexError:
                collisionInt = -1

        elif collision_side.lower() == "l":
            try:
                playerPos = (math.floor((player.y + player.height / 2) / 16), math.floor((player.x) / 16))
                collisionInt = self.collision_intgrid(intgrid, playerPos, collision_block_side)

                if collisionInt == 0:
                    playerPos = (math.floor((player.y) / 16), math.floor((player.x) / 16))
                    collisionInt = self.collision_intgrid(intgrid, playerPos, collision_block_side)
                if collisionInt == 0:
                    playerPos = (math.floor((player.y + player.height) / 16), math.floor((player.x) / 16))
                    collisionInt = self.collision_intgrid(intgrid, playerPos, collision_block_side)
            except IndexError:
                collisionInt = -1

        elif collision_side.lower() == "r":
            try:
                playerPos = (math.floor((player.y + player.height / 2) / 16), math.floor((player.x + player.width) / 16))
                collisionInt = self.collision_intgrid(intgrid, playerPos, collision_block_side)

                if collisionInt == 0:
                    playerPos = (math.floor((player.y) / 16), math.floor((player.x + player.width) / 16))
                    collisionInt = self.collision_intgrid(intgrid, playerPos, collision_block_side)
                if collisionInt == 0:
                    playerPos = (math.floor((player.y + player.height) / 16), math.floor((player.x + player.width) / 16))
                    collisionInt = self.collision_intgrid(intgrid, playerPos, collision_block_side)
            except IndexError:
                collisionInt = -1

        else:
            raise NameError(f'String "{collision_side}" does not match up with directions "u", "d", "l" or "r".')

        return collisionInt
    
    def handle_action(self, game: Game):
        # Variables:
        # self.pos, self.vel, self.gravity, self.jumpheight, self.isonground

        posx, posy = self.pos
        velx, vely = self.vel

        if game.GMCTRL.pushed[INP.moveleft]:
            velx -= self.walkingspeed
        if game.GMCTRL.pushed[INP.moveright]:
            velx += self.walkingspeed
        if game.GMCTRL.pushed[INP.jump]:
            vely -= self.walkingspeed
        if game.GMCTRL.pushed[INP.sneak]:
            vely += self.walkingspeed

        velx /= self.horizontal_movement_deacceleration
        vely /= self.vertical_movement_deacceleration

        collisions = {
            "d": self.check_collisions(game, game.LEVEL.LVL_INTS.solid, self.pos_to_rect((posx, posy)), self.pos_to_rect(self.previous_pos), collision_side='d'),
            "u": self.check_collisions(game, game.LEVEL.LVL_INTS.solid, self.pos_to_rect((posx, posy)), self.pos_to_rect(self.previous_pos), collision_side='u'),
            "l": self.check_collisions(game, game.LEVEL.LVL_INTS.solid, self.pos_to_rect((posx, posy)), self.pos_to_rect(self.previous_pos), collision_side='l'),
            "r": self.check_collisions(game, game.LEVEL.LVL_INTS.solid, self.pos_to_rect((posx, posy)), self.pos_to_rect(self.previous_pos), collision_side='r')
        }

        self.previous_pos = (posx, posy)

        posx += velx
        posy += vely
        
        collisions_filtered = {
            "d": self.check_collisions(game, game.LEVEL.LVL_INTS.solid, self.pos_to_rect((posx, posy)), self.pos_to_rect(self.previous_pos), collision_side='d', collision_block_side='d'),
            "u": self.check_collisions(game, game.LEVEL.LVL_INTS.solid, self.pos_to_rect((posx, posy)), self.pos_to_rect(self.previous_pos), collision_side='u', collision_block_side='u'),
            "l": self.check_collisions(game, game.LEVEL.LVL_INTS.solid, self.pos_to_rect((posx, posy)), self.pos_to_rect(self.previous_pos), collision_side='l', collision_block_side='l'),
            "r": self.check_collisions(game, game.LEVEL.LVL_INTS.solid, self.pos_to_rect((posx, posy)), self.pos_to_rect(self.previous_pos), collision_side='r', collision_block_side='r'),
        }


        """
        if collisions_filtered["l"] != 0:
            while collisions_filtered["l"] != 0 and timesIncremented < 16:
                posx += 1
                timesIncremented += 1
                collisions_filtered["l"] = self.check_collisions(game, game.LEVEL.LVL_INTS.solid, self.pos_to_rect((posx, posy)), collision_side='l', collision_block_side='l')
            velx = 0

        if collisions_filtered["r"] != 0:
            while collisions_filtered["r"] != 0 and timesIncremented < 16:
                posx -= 1
                timesIncremented += 1
                collisions_filtered["r"] = self.check_collisions(game, game.LEVEL.LVL_INTS.solid, self.pos_to_rect((posx, posy)), collision_side='r', collision_block_side='r')
            velx = 0
        
        if collisions_filtered["d"] != 0:
            while collisions_filtered["d"] != 0 and timesIncremented < 16:
                posy -= 1
                timesIncremented += 1
                collisions_filtered["d"] = self.check_collisions(game, game.LEVEL.LVL_INTS.solid, self.pos_to_rect((posx, posy)), collision_side='d', collision_block_side='d')
            vely = 0

        if collisions_filtered["u"] != 0:
            while collisions_filtered["u"] != 0 and timesIncremented < 16:
                posy += 1
                timesIncremented += 1
                collisions_filtered["u"] = self.check_collisions(game, game.LEVEL.LVL_INTS.solid, self.pos_to_rect((posx, posy)), collision_side='u', collision_block_side='u')
            vely = 0
        """
        #print(f"\
        #Collision up: {collisions['u']}, Collision down: {collisions['d']}, Collision left: {collisions['l']}, Collision right: {collisions['r']} \
        #Filtered collision up: {collisions_filtered["u"]}, Collision down: {collisions_filtered["d"]}, Collision left: {collisions_filtered["l"]}, Collision right: {collisions_filtered["r"]}")
        #posx, posy, velx, vely = self.handle_collisions(game, (posx, posy), (velx, vely), collisions)

        self.pos = posx, posy
        self.vel = velx, vely
        
    def handle_anim(self, game: Game):
        pass
    