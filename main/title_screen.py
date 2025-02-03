import time, pygame

menu_title = pygame.image.load("main/assets/gui/title.png")

class class_GUI():
    def __init__(self):
        self.current_menu_screen = 0
        self.menu_screen = [
            {
                ""
                "rows": 2,
            }
        ]
        self.selected_button = 0
        self.selected_button_maximum = 3
        self.controls_previously_pressed = [
            False,
            False,
            False,
            False
        ]
        self.anim = [
            0, 0, 0
        ]
        self.surface = pygame.Surface((1, 1))
        self.scale = 5

        class Assets():
            def __init__(self):
                self.pixelfont = 0
                self.menu_buttons = [
                    pygame.image.load("main/assets/gui/button_a_default.png"),
                    pygame.image.load("main/assets/gui/button_b_default.png"),
                    pygame.image.load("main/assets/gui/button_x_default.png"),
                    pygame.image.load("main/assets/gui/button_y_default.png"),
                ]

                self.menu_buttons_selected = [
                    pygame.image.load("main/assets/gui/button_a_hover.png"),
                    pygame.image.load("main/assets/gui/button_b_hover.png"),
                    pygame.image.load("main/assets/gui/button_x_hover.png"),
                    pygame.image.load("main/assets/gui/button_y_hover.png"),
                ]

                self.menu_buttons_push = [
                    pygame.image.load("main/assets/gui/button_a_push.png"),
                    pygame.image.load("main/assets/gui/button_b_push.png"),
                    pygame.image.load("main/assets/gui/button_x_push.png"),
                    pygame.image.load("main/assets/gui/button_y_push.png"),
                ]
        self.assets = Assets()
        self.time_passed = 0
GUI = class_GUI()

for i2 in range(len(GUI.assets.menu_buttons)):
    i = GUI.assets.menu_buttons[i2]
    GUI.assets.menu_buttons[i2] = pygame.transform.scale(i, (i.get_width() * GUI.scale, i.get_height() * GUI.scale))

for i2 in range(len(GUI.assets.menu_buttons_selected)):
    i = GUI.assets.menu_buttons_selected[i2]
    GUI.assets.menu_buttons_selected[i2] = pygame.transform.scale(i, (i.get_width() * GUI.scale, i.get_height() * GUI.scale))

for i2 in range(len(GUI.assets.menu_buttons_push)):
    i = GUI.assets.menu_buttons_push[i2]
    GUI.assets.menu_buttons_push[i2] = pygame.transform.scale(i, (i.get_width() * GUI.scale, i.get_height() * GUI.scale))

menu_title = pygame.transform.scale(menu_title, (GUI.assets.menu_buttons[0].get_width() * 2 + GUI.scale, GUI.assets.menu_buttons[0].get_height() * 2 + GUI.scale, ))

from control import INP

print(str(time.time_ns()) + " Initialising title_screen.py")

def draw_menu_screen(WIN, controls, pyg):


    if GUI.time_passed == 0:
        GUI.surface = pygame.Surface(WIN.get_size())
        GUI.anim[0] = WIN.get_width()
        GUI.anim[1] = WIN.get_width()
        GUI.anim[2] = WIN.get_width()

        GUI.assets.pixelfont = pyg.font.Font('main/assets/font.ttf', 36)
    GUI.time_passed += 1

    if controls[INP.GUI_Up]:
        if GUI.controls_previously_pressed[0]:
            pass
        else:
            GUI.controls_previously_pressed[0] = True
            GUI.selected_button -= 1
    else: GUI.controls_previously_pressed[0] = False

    if controls[INP.GUI_Down]:
        if GUI.controls_previously_pressed[1]:
            pass
        else:
            GUI.controls_previously_pressed[1] = True
            GUI.selected_button += 1
    else: GUI.controls_previously_pressed[1] = False

    if controls[INP.GUI_Left] or controls[INP.item_left]:
        if GUI.controls_previously_pressed[2]:
            pass
        else:
            GUI.controls_previously_pressed[2] = True
            GUI.selected_button -= 2
    else: GUI.controls_previously_pressed[2] = False

    if controls[INP.GUI_Right] or controls[INP.item_right]:
        if GUI.controls_previously_pressed[3]:
            pass
        else:
            GUI.controls_previously_pressed[3] = True
            GUI.selected_button += 2
    else: GUI.controls_previously_pressed[3] = False

    while GUI.selected_button > GUI.selected_button_maximum:
        GUI.selected_button -= GUI.selected_button_maximum + 1
    while GUI.selected_button < 0:
        GUI.selected_button += GUI.selected_button_maximum + 1

    if controls[INP.GUI_A]:
        GUI.selected_button = 0
        GUI.surface = pygame.Surface(WIN.get_size())
    if controls[INP.GUI_B]:
        GUI.selected_button = 1
        GUI.surface = pygame.Surface(WIN.get_size())
    if controls[INP.GUI_X]:
        GUI.selected_button = 2
        GUI.surface = pygame.Surface(WIN.get_size())
    if controls[INP.GUI_Y]:
        GUI.selected_button = 3
        GUI.surface = pygame.Surface(WIN.get_size())

    # Button A
    tmp_ispushed = controls[INP.GUI_A]
    tmp_imgs = (GUI.assets.menu_buttons_push if tmp_ispushed else (GUI.assets.menu_buttons_selected if GUI.selected_button == 0 else GUI.assets.menu_buttons))
    GUI.surface.blit(tmp_imgs[0], (
        WIN.get_width() / 2 - (GUI.scale + GUI.assets.menu_buttons[0].get_width() * 2) / 2 + (GUI.scale + GUI.assets.menu_buttons[1].get_width()) * 0 - GUI.anim[1],
        WIN.get_height() / 2 - (GUI.scale + GUI.assets.menu_buttons[0].get_height() * -1) / 2 + (GUI.scale + GUI.assets.menu_buttons[1].get_height()) * 0
    ))
    tmp_fontsurf = GUI.assets.pixelfont.render(f"Start game", True, (255, 255, 255))
    tmp_fontsurf = pygame.transform.scale(tmp_fontsurf, (
        (tmp_fontsurf.get_width() / tmp_fontsurf.get_height()) * (GUI.scale * 8),
        GUI.scale * 8
    ))
    GUI.surface.blit(tmp_fontsurf, (
        WIN.get_width() / 2 - (GUI.scale + GUI.assets.menu_buttons[0].get_width() * 2) / 2 + (GUI.scale + GUI.assets.menu_buttons[1].get_width()) * 0 - GUI.anim[1]         + GUI.assets.menu_buttons[0].get_width() / 2 - tmp_fontsurf.get_width() / 2,
        WIN.get_height() / 2 - (GUI.scale + GUI.assets.menu_buttons[0].get_height() * -1) / 2 + (GUI.scale + GUI.assets.menu_buttons[1].get_height()) * 0                   + 4 * GUI.scale + (GUI.scale * 2 if tmp_ispushed else 0)
    ))

    # Button B
    tmp_ispushed = controls[INP.GUI_B]
    tmp_imgs = (GUI.assets.menu_buttons_push if tmp_ispushed else (GUI.assets.menu_buttons_selected if GUI.selected_button == 1 else GUI.assets.menu_buttons))
    GUI.surface.blit(tmp_imgs[1], (
        WIN.get_width() / 2 - (GUI.scale + GUI.assets.menu_buttons[1].get_width() * 2) / 2 + (GUI.scale + GUI.assets.menu_buttons[1].get_width()) * 0 + GUI.anim[2],
        WIN.get_height() / 2 - (GUI.scale + GUI.assets.menu_buttons[1].get_height() * -1) / 2 + (GUI.scale + GUI.assets.menu_buttons[1].get_height()) * 1
    ))
    tmp_fontsurf = GUI.assets.pixelfont.render(f"Exit", True, (255, 255, 255))
    tmp_fontsurf = pygame.transform.scale(tmp_fontsurf, (
        (tmp_fontsurf.get_width() / tmp_fontsurf.get_height()) * (GUI.scale * 8),
        GUI.scale * 8
    ))
    GUI.surface.blit(tmp_fontsurf, (
        WIN.get_width() / 2 - (GUI.scale + GUI.assets.menu_buttons[0].get_width() * 2) / 2 + (GUI.scale + GUI.assets.menu_buttons[1].get_width()) * 0 + GUI.anim[2]         + GUI.assets.menu_buttons[0].get_width() / 2 - tmp_fontsurf.get_width() / 2,
        WIN.get_height() / 2 - (GUI.scale + GUI.assets.menu_buttons[0].get_height() * -1) / 2 + (GUI.scale + GUI.assets.menu_buttons[1].get_height()) * 1                   + 4 * GUI.scale + (GUI.scale * 2 if tmp_ispushed else 0)
    ))

    # Button X
    tmp_ispushed = controls[INP.GUI_X]
    tmp_imgs = (GUI.assets.menu_buttons_push if tmp_ispushed else (GUI.assets.menu_buttons_selected if GUI.selected_button == 2 else GUI.assets.menu_buttons))
    GUI.surface.blit(tmp_imgs[2], (
        WIN.get_width() / 2 - (GUI.scale + GUI.assets.menu_buttons[2].get_width() * 2) / 2 + (GUI.scale + GUI.assets.menu_buttons[1].get_width()) * 1 - GUI.anim[1],
        WIN.get_height() / 2 - (GUI.scale + GUI.assets.menu_buttons[2].get_height() * -1) / 2 + (GUI.scale + GUI.assets.menu_buttons[1].get_height()) * 0
    ))
    tmp_fontsurf = GUI.assets.pixelfont.render(f"Options", True, (255, 255, 255))
    tmp_fontsurf = pygame.transform.scale(tmp_fontsurf, (
        (tmp_fontsurf.get_width() / tmp_fontsurf.get_height()) * (GUI.scale * 8),
        GUI.scale * 8
    ))
    GUI.surface.blit(tmp_fontsurf, (
        WIN.get_width() / 2 - (GUI.scale + GUI.assets.menu_buttons[0].get_width() * 2) / 2 + (GUI.scale + GUI.assets.menu_buttons[1].get_width()) * 1 - GUI.anim[1]         + GUI.assets.menu_buttons[0].get_width() / 2 - tmp_fontsurf.get_width() / 2,
        WIN.get_height() / 2 - (GUI.scale + GUI.assets.menu_buttons[0].get_height() * -1) / 2 + (GUI.scale + GUI.assets.menu_buttons[1].get_height()) * 0                   + 4 * GUI.scale + (GUI.scale * 2 if tmp_ispushed else 0)
    ))

    # Button Y
    tmp_ispushed = controls[INP.GUI_Y]
    tmp_imgs = (GUI.assets.menu_buttons_push if tmp_ispushed else (GUI.assets.menu_buttons_selected if GUI.selected_button == 3 else GUI.assets.menu_buttons))
    GUI.surface.blit(tmp_imgs[3], (
        WIN.get_width() / 2 - (GUI.scale + GUI.assets.menu_buttons[3].get_width() * 2) / 2 + (GUI.scale + GUI.assets.menu_buttons[1].get_width()) * 1 + GUI.anim[2],
        WIN.get_height() / 2 - (GUI.scale + GUI.assets.menu_buttons[3].get_height() * -1) / 2 + (GUI.scale + GUI.assets.menu_buttons[1].get_height()) * 1
    ))
    tmp_fontsurf = GUI.assets.pixelfont.render(f"Credits", True, (255, 255, 255))
    tmp_fontsurf = pygame.transform.scale(tmp_fontsurf, (
        (tmp_fontsurf.get_width() / tmp_fontsurf.get_height()) * (GUI.scale * 8),
        GUI.scale * 8
    ))
    GUI.surface.blit(tmp_fontsurf, (
        WIN.get_width() / 2 - (GUI.scale + GUI.assets.menu_buttons[0].get_width() * 2) / 2 + (GUI.scale + GUI.assets.menu_buttons[1].get_width()) * 1 + GUI.anim[2]         + GUI.assets.menu_buttons[0].get_width() / 2 - tmp_fontsurf.get_width() / 2,
        WIN.get_height() / 2 - (GUI.scale + GUI.assets.menu_buttons[0].get_height() * -1) / 2 + (GUI.scale + GUI.assets.menu_buttons[1].get_height()) * 1                   + 4 * GUI.scale + (GUI.scale * 2 if tmp_ispushed else 0)
    ))

    # Menu Title
    GUI.surface.blit(menu_title, (
        WIN.get_width() / 2 - (GUI.scale + GUI.assets.menu_buttons[3].get_width() * 2) / 2 + (GUI.scale + GUI.assets.menu_buttons[1].get_width()) * 0 + GUI.anim[0],
        WIN.get_height() / 2 - (GUI.scale + GUI.assets.menu_buttons[3].get_height() * 1) / 2 + (GUI.scale + GUI.assets.menu_buttons[1].get_height()) * -1
    ))

    GUI.anim[0] /= 1.05

    if GUI.time_passed > 20: GUI.anim[1] /= 1.05
    if GUI.time_passed > 40: GUI.anim[2] /= 1.05

    WIN.blit(GUI.surface, (0, 0))
    
    GUI.surface = pygame.Surface(WIN.get_size())

    print(GUI.controls_previously_pressed)

print(str(time.time_ns()) + " Done")