import control
import game_classes as GAMEDATA
import input_ID as INP
import pygame
import title_screen as TITLESCREEN

def start_game(WIN):
    GAMEDATA.surfaces.GUI = pygame.surface.Surface(WIN.get_size(), pygame.SRCALPHA)
    GAMEDATA.surfaces.CHARACTERS = pygame.surface.Surface(WIN.get_size(), pygame.SRCALPHA)
    GAMEDATA.surfaces.FOREGROUND = pygame.surface.Surface(WIN.get_size(), pygame.SRCALPHA)
    GAMEDATA.surfaces.BACKGROUND = pygame.surface.Surface(WIN.get_size(), pygame.SRCALPHA)
    GAMEDATA.surfaces.GUI.fill((0, 0, 0, 0))
    GAMEDATA.surfaces.CHARACTERS.fill((0, 0, 0, 0))
    GAMEDATA.surfaces.FOREGROUND.fill((0, 0, 0, 0))
    GAMEDATA.surfaces.BACKGROUND.fill((0, 0, 0, 0))
    GAMEDATA.surfaces.GUI.fill((0, 0, 0, 0))

class Data():
    def __init__(self):
        self.ISPAUSED = True
        self.GMCTRL = []
data = Data()

def draw_game(WIN):
    data.GMCTRL = control.GMCTRL

    # Refresh these surfaces
    GAMEDATA.surfaces.BACKGROUND = pygame.surface.Surface(WIN.get_size(), pygame.SRCALPHA)
    GAMEDATA.surfaces.BACKGROUND.fill((0, 0, 0, 128))

    GAMEDATA.surfaces.CHARACTERS = pygame.surface.Surface(WIN.get_size(), pygame.SRCALPHA)
    GAMEDATA.surfaces.CHARACTERS.fill((0, 0, 0, 128))

    GAMEDATA.surfaces.FOREGROUND = pygame.surface.Surface(WIN.get_size(), pygame.SRCALPHA)
    GAMEDATA.surfaces.FOREGROUND.fill((0, 0, 0, 128))

    GAMEDATA.surfaces.GUI = pygame.surface.Surface(WIN.get_size(), pygame.SRCALPHA)

    # If it has "ingame" and isn't directly ingame then it must be paused
    if TITLESCREEN.title_screen_layout.layout_pausedgame in TITLESCREEN.GUI.current_menu_screen and TITLESCREEN.GUI.current_menu_screen != "ingame":
        data.ISPAUSED = True

    if data.GMCTRL.tapped[INP.pausegame] and TITLESCREEN.GUI.current_menu_screen:
        data.ISPAUSED = not data.ISPAUSED

        # If it's paused, then make it the default pause menu.
        if data.ISPAUSED:
            TITLESCREEN.GUI.reset_anim(GAMEDATA.surfaces)
            TITLESCREEN.GUI.current_menu_screen = TITLESCREEN.title_screen_layout.layout_pausedgame

    # If ingame and unpaused then handle action
    if TITLESCREEN.GUI.current_menu_screen == TITLESCREEN.title_screen_layout.layout_ingame:
        GAMEDATA.player.handle_action(control.GMCTRL)

    # If ingame then draw level
    if TITLESCREEN.title_screen_layout.layout_ingame in TITLESCREEN.GUI.current_menu_screen:
        if control.GMCTRL.windowResized:
            GAMEDATA.lvl.draw_refresh(WIN)
        GAMEDATA.lvl.draw()

    if TITLESCREEN.GUI.current_menu_screen != TITLESCREEN.title_screen_layout.layout_ingame:
        TITLESCREEN.draw_menu_screen(data, GAMEDATA.surfaces)

    WIN.blit(GAMEDATA.surfaces.BACKGROUND, (0, 0))
    WIN.blit(GAMEDATA.surfaces.CHARACTERS, (0, 0))
    WIN.blit(GAMEDATA.surfaces.GUI, (0, 0))