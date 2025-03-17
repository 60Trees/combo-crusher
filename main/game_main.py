import game_classes as GAMECLASS
import input_ID as INP
import pygame  # noqa: F401

def draw_game(game: GAMECLASS.Game):
    game.timesincestart += 1

    if game.GUI.layout.ingame not in game.GUI.current_menu_screen:
        game.timeplaying = 0

    # If it has "ingame" and isn't directly ingame then it must be paused
    if game.GUI.layout.pausegame in game.GUI.current_menu_screen and game.GUI.current_menu_screen != "ingame":
        game.ISPAUSED = True

    if game.GMCTRL.tapped[INP.pausegame] and game.GUI.current_menu_screen:
        game.ISPAUSED = not game.ISPAUSED

        # If it's paused, then make it the default pause menu.
        if game.ISPAUSED:
            game.GUI.reset_anim(game)
            game.GUI.current_menu_screen = game.GUI.layout.pausegame

    # If ingame and unpaused then handle action
    if game.GUI.current_menu_screen == game.GUI.layout.ingame:
        game.PLAYER.handle_action(game)
        game.timeplayed += 1
        game.timeplaying += 1

    # If ingame then draw level
    if game.GUI.layout.ingame in game.GUI.current_menu_screen:
        if game.GMCTRL.windowResized:
            game.LEVEL.draw_refresh(game)
        game.LEVEL.draw(game)

    if game.GUI.current_menu_screen != game.GUI.layout.ingame:
        game.GUI.draw_menu_screen(game)