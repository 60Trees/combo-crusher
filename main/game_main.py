import control
import game_classes as GAMEDATA
import input_ID as INP
import pygame  # noqa: F401
import title_screen as TITLESCREEN

def start_game(WIN):
    pass

class Data():
    def __init__(self):
        self.ISPAUSED = True
        self.GMCTRL = []
data = Data()

def draw_game(WIN):
    data.GMCTRL = control.GMCTRL

    # If it has "ingame" and isn't directly ingame then it must be paused
    if TITLESCREEN.title_screen_layout.layout_pausedgame in TITLESCREEN.GUI.current_menu_screen and TITLESCREEN.GUI.current_menu_screen != "ingame":
        data.ISPAUSED = True

    if data.GMCTRL.tapped[INP.pausegame] and TITLESCREEN.GUI.current_menu_screen:
        data.ISPAUSED = not data.ISPAUSED

        # If it's paused, then make it the default pause menu.
        if data.ISPAUSED:
            TITLESCREEN.GUI.reset_anim(WIN)
            TITLESCREEN.GUI.current_menu_screen = TITLESCREEN.title_screen_layout.layout_pausedgame

    # If ingame and unpaused then handle action
    if TITLESCREEN.GUI.current_menu_screen == TITLESCREEN.title_screen_layout.layout_ingame:
        GAMEDATA.player.handle_action(control.GMCTRL)

    # If ingame then draw level
    if TITLESCREEN.title_screen_layout.layout_ingame in TITLESCREEN.GUI.current_menu_screen:
        if control.GMCTRL.windowResized:
            GAMEDATA.lvl.draw_refresh(WIN)
        GAMEDATA.lvl.draw(WIN)

    if TITLESCREEN.GUI.current_menu_screen != TITLESCREEN.title_screen_layout.layout_ingame:
        TITLESCREEN.draw_menu_screen(data, WIN)