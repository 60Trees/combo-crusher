import time
import pygame

import title_screen  # noqa: F401
import INP
import game_classes as GAME

menu_title = pygame.image.load("main/assets/gui/title.png")

floor_collision = 0
ceiling_collision = 1

left = False
right = True

print(str(time.time_ns()) + " Initialising title_screen.py")

def draw_game(WIN, CTRL, isPaused):
    ispausing = isPaused
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
    
    if not isPaused:
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
            (round(GAME.player.pos[0]) * GAME.camera.zoom_in + GAME.camera.pos[0] * GAME.camera.zoom_in) - surf.get_width() * GAME.camera.zoom_in / 2,
            (round(GAME.player.pos[1]) * GAME.camera.zoom_in + GAME.camera.pos[1] * GAME.camera.zoom_in) - surf.get_height() * GAME.camera.zoom_in
        )
    )

    for i in GAME.lvl.FLOORS:
        pygame.draw.line(
            GAME.surface.characters,
            (255, 0, 0),
            (
                i[0][0] * GAME.camera.zoom_in + GAME.camera.pos[0] * GAME.camera.zoom_in,
                i[0][1] * GAME.camera.zoom_in + GAME.camera.pos[1] * GAME.camera.zoom_in
            ),
            (
                i[1][0] * GAME.camera.zoom_in + GAME.camera.pos[0] * GAME.camera.zoom_in,
                i[1][1] * GAME.camera.zoom_in + GAME.camera.pos[1] * GAME.camera.zoom_in
            )
        )
    for i in GAME.lvl.CEILINGS:
        pygame.draw.line(
            GAME.surface.characters,
            (0, 0, 255),
            (
                i[0][0] * GAME.camera.zoom_in + GAME.camera.pos[0] * GAME.camera.zoom_in,
                i[0][1] * GAME.camera.zoom_in + GAME.camera.pos[1] * GAME.camera.zoom_in
            ),
            (
                i[1][0] * GAME.camera.zoom_in + GAME.camera.pos[0] * GAME.camera.zoom_in,
                i[1][1] * GAME.camera.zoom_in + GAME.camera.pos[1] * GAME.camera.zoom_in
            )
        )
    
    #pygame.draw.line(win, (255, 0, 0), (0, 0), (500, 500), 5)
    #               SURFACE  colour    startpos   endpos    thickness

    #print(f"Printing player at X={GAME.player.pos[0] * GAME.camera.zoom_in + GAME.camera.pos[0] * GAME.camera.zoom_in}, Y={GAME.player.pos[1] * GAME.camera.zoom_in + GAME.camera.pos[1] * GAME.camera.zoom_in}")

    if not isPaused:
        if CTRL[INP.minimap]:
            GAME.player.pos = (0, -50)
            GAME.player.vel = (0, 0)
        GAME.player.animupdatetimer += 1
        #print(f"Before: Player pos={GAME.player.pos},vel={GAME.player.vel},isOnGr={GAME.player.isonground},actionstate={GAME.player.actionstate}")
        GAME.player.handle_action(CTRL)
        #print(f"After:  Player pos={GAME.player.pos},vel={GAME.player.vel},isOnGr={GAME.player.isonground},actionstate={GAME.player.actionstate}")
        if GAME.player.animupdatetimer > GAME.player.animupdatetimer_maximum:
            GAME.player.handle_anim()
            #print(f"Updating anim, animstate={GAME.player.animstate}, facing={tmp}, actionstate={GAME.player.actionstate}")
            GAME.player.animupdatetimer = 0

    if CTRL[INP.pausegame] and GAME.previouslypausedgame:
        print("Pausing GAMEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEE")
        ispausing = not ispausing
        GAME.previouslypausedgame = True
    elif not CTRL[INP.pausegame]:
        GAME.previouslypausedgame = False

    WIN.blit(GAME.surface.background, (0, 0))
    WIN.blit(GAME.surface.characters, (0, 0))
    WIN.blit(GAME.surface.foreground, (0, 0))
    WIN.blit(GAME.surface.gui, (0, 0))

    return ispausing

print(str(time.time_ns()) + " Done")