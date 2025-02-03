import time, pygame

menu_title = pygame.image.load("main/assets/gui/title.png")

class class_GUI():
    def __init__(self):
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
def draw_menu_screen(WIN, controls):

    GUI.time_passed += 1

    if GUI.time_passed == 0:
        GUI.surface = pygame.Surface(WIN.get_size())
        GUI.anim[0] = WIN.get_width()
        GUI.anim[1] = WIN.get_width()
        GUI.anim[2] = WIN.get_width()

    if controls[INP.GUI_Up]:
        if GUI.controls_previously_pressed[0]:
            pass
        else:
            GUI.controls_previously_pressed[0] = True
            GUI.selected_button -= 1
    else: controls[INP.GUI_Up] = False

    if controls[INP.GUI_Down]:
        if GUI.controls_previously_pressed[1]:
            pass
        else:
            GUI.controls_previously_pressed[1] = True
            GUI.selected_button += 1
    else: controls[INP.GUI_Down] = False

    if controls[INP.GUI_Left]:
        if GUI.controls_previously_pressed[2]:
            pass
        else:
            GUI.controls_previously_pressed[2] = True
            GUI.selected_button -= 2
    else: controls[INP.GUI_Left] = False

    if controls[INP.GUI_Right]:
        if GUI.controls_previously_pressed[3]:
            pass
        else:
            GUI.controls_previously_pressed[3] = True
            GUI.selected_button += 2
    else: controls[INP.GUI_Right] = False

    while GUI.selected_button >= 4:
        GUI.selected_button -= 4
    while GUI.selected_button < 0:
        GUI.selected_button += 4

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

    tmp_imgs = (GUI.assets.menu_buttons_push if controls[INP.GUI_A] else (GUI.assets.menu_buttons_selected if GUI.selected_button == 0 else GUI.assets.menu_buttons))
    GUI_WIN.blit(tmp_imgs[0], (
        WIN.get_width() / 2 - (GUI.scale + GUI.assets.menu_buttons[0].get_width() * 2) / 2 + (GUI.scale + GUI.assets.menu_buttons[1].get_width()) * 0 - GUI.anim[1],
        WIN.get_height() / 2 - (GUI.scale + GUI.assets.menu_buttons[0].get_height() * -1) / 2 + (GUI.scale + GUI.assets.menu_buttons[1].get_height()) * 0
    ))

    tmp_imgs = (GUI.assets.menu_buttons_push if controls[INP.GUI_B] else (GUI.assets.menu_buttons_selected if GUI.selected_button == 1 else GUI.assets.menu_buttons))
    GUI_WIN.blit(tmp_imgs[1], (
        WIN.get_width() / 2 - (GUI.scale + GUI.assets.menu_buttons[1].get_width() * 2) / 2 + (GUI.scale + GUI.assets.menu_buttons[1].get_width()) * 0 + GUI.anim[2],
        WIN.get_height() / 2 - (GUI.scale + GUI.assets.menu_buttons[1].get_height() * -1) / 2 + (GUI.scale + GUI.assets.menu_buttons[1].get_height()) * 1
    ))

    tmp_imgs = (GUI.assets.menu_buttons_push if controls[INP.GUI_X] else (GUI.assets.menu_buttons_selected if GUI.selected_button == 2 else GUI.assets.menu_buttons))
    GUI_WIN.blit(tmp_imgs[2], (
        WIN.get_width() / 2 - (GUI.scale + GUI.assets.menu_buttons[2].get_width() * 2) / 2 + (GUI.scale + GUI.assets.menu_buttons[1].get_width()) * 1 - GUI.anim[1],
        WIN.get_height() / 2 - (GUI.scale + GUI.assets.menu_buttons[2].get_height() * -1) / 2 + (GUI.scale + GUI.assets.menu_buttons[1].get_height()) * 0
    ))

    tmp_imgs = (GUI.assets.menu_buttons_push if controls[INP.GUI_Y] else (GUI.assets.menu_buttons_selected if GUI.selected_button == 3 else GUI.assets.menu_buttons))
    GUI_WIN.blit(tmp_imgs[3], (
        WIN.get_width() / 2 - (GUI.scale + GUI.assets.menu_buttons[3].get_width() * 2) / 2 + (GUI.scale + GUI.assets.menu_buttons[1].get_width()) * 1 + GUI.anim[2],
        WIN.get_height() / 2 - (GUI.scale + GUI.assets.menu_buttons[3].get_height() * -1) / 2 + (GUI.scale + GUI.assets.menu_buttons[1].get_height()) * 1
    ))

    GUI_WIN.blit(menu_title, (
        WIN.get_width() / 2 - (GUI.scale + GUI.assets.menu_buttons[3].get_width() * 2) / 2 + (GUI.scale + GUI.assets.menu_buttons[1].get_width()) * 0 + GUI.anim[0],
        WIN.get_height() / 2 - (GUI.scale + GUI.assets.menu_buttons[3].get_height() * 1) / 2 + (GUI.scale + GUI.assets.menu_buttons[1].get_height()) * -1
    ))

    GUI.anim[0] /= 1.05

    if GUI.time_passed > 20: GUI.anim[1] /= 1.05
    if GUI.time_passed > 40: GUI.anim[2] /= 1.05

    WIN.blit(GUI_WIN, (0, 0))
    
    GUI_WIN = pygame.Surface(WIN.get_size())

print(str(time.time_ns()) + " Done")