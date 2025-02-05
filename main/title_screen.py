import time, pygame, json_func

menu_title = pygame.image.load("main/assets/gui/title.png")
from control import INP

class class_GUI():
    def __init__(self):
        self.timer = 0
        self.current_menu_screen = "main_menu"
        self.menu_screen = {
            "main_menu": {
                "starting_point": (2, -1),
                "buttons": [
                    {
                        "image": "menu_title",
                        "image_hover": None,
                        "image_push": None,
                        "anim": 0,
                        "anim_positive": True,
                        "pos_multiplier": (0, -2),
                        "button_assignment": None,
                        "text": None,
                        "button_push": None,
                        "button_push_menu_screen": None
                    },
                    {
                        "image": "GUI.assets.menu_buttons[0]",
                        "image_hover": "GUI.assets.menu_buttons_selected[0]",
                        "image_push": "GUI.assets.menu_buttons_push[0]",
                        "anim": 1,
                        "anim_positive": False,
                        "pos_multiplier": (0, 0),
                        "button_assignment": 0,
                        "text": ("Start Game", True, (255, 255, 255)),
                        "button_push": INP.GUI_A,
                        "button_push_menu_screen": "main_menu/choose_gamemode"
                    },
                    {
                        "image": "GUI.assets.menu_buttons[1]",
                        "image_hover": "GUI.assets.menu_buttons_selected[1]",
                        "image_push": "GUI.assets.menu_buttons_push[1]",
                        "anim": 2,
                        "anim_positive": True,
                        "pos_multiplier": (0, 1),
                        "button_assignment": 1,
                        "text": ("Exit", True, (255, 255, 255)),
                        "button_push": INP.GUI_B,
                        "button_push_menu_screen": "main_menu"
                    },
                    {
                        "image": "GUI.assets.menu_buttons[2]",
                        "image_hover": "GUI.assets.menu_buttons_selected[2]",
                        "image_push": "GUI.assets.menu_buttons_push[2]",
                        "anim": 1,
                        "anim_positive": False,
                        "pos_multiplier": (1, 0),
                        "button_assignment": 2,
                        "text": ("Settings", True, (255, 255, 255)),
                        "button_push": INP.GUI_X,
                        "button_push_menu_screen": "main_menu"
                    },
                    {
                        "image": "GUI.assets.menu_buttons[3]",
                        "image_hover": "GUI.assets.menu_buttons_selected[3]",
                        "image_push": "GUI.assets.menu_buttons_push[3]",
                        "anim": 2,
                        "anim_positive": True,
                        "pos_multiplier": (1, 1),
                        "button_assignment": 3,
                        "text": ("Credits", True, (255, 255, 255)),
                        "button_push": INP.GUI_Y,
                        "button_push_menu_screen": "main_menu"
                    },
                ]
            }
        }
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

    # Menu title
    i = 0
    tmp_ispushed = False if GUI.menu_screen[GUI.current_menu_screen]["buttons"][i]["button_assignment"] == None else \
        controls[GUI.menu_screen[GUI.current_menu_screen]["buttons"][i]["button_push"]] and GUI.selected_button == GUI.menu_screen[GUI.current_menu_screen]["buttons"][i]["button_assignment"]
    GUI.timer += 2 if tmp_ispushed else 0
    tmp_imgs = (eval(GUI.menu_screen[GUI.current_menu_screen]["buttons"][i]["image_push"]) if tmp_ispushed else (eval(GUI.menu_screen[GUI.current_menu_screen]["buttons"][i]["image_hover"]) if GUI.selected_button == GUI.menu_screen[GUI.current_menu_screen]["buttons"][i]["button_assignment"] else eval(GUI.menu_screen[GUI.current_menu_screen]["buttons"][i]["image"])))
    GUI.surface.blit(tmp_imgs, (
        WIN.get_width() / 2 - (GUI.scale + GUI.assets.menu_buttons[0].get_width() * GUI.menu_screen[GUI.current_menu_screen]["starting_point"][0]) / 2 + (GUI.scale + GUI.assets.menu_buttons[0].get_width()) * GUI.menu_screen[GUI.current_menu_screen]["buttons"][i]["pos_multiplier"][0] + (GUI.menu_screen[GUI.current_menu_screen]["buttons"][i]["anim"] * 1 if GUI.menu_screen[GUI.current_menu_screen]["buttons"][i]["anim_positive"] else -1),
        WIN.get_height() / 2 - (GUI.scale + GUI.assets.menu_buttons[0].get_height() * GUI.menu_screen[GUI.current_menu_screen]["starting_point"][1]) / 2 + (GUI.scale + GUI.assets.menu_buttons[0].get_height()) * GUI.menu_screen[GUI.current_menu_screen]["buttons"][i]["pos_multiplier"][1]
    ))
    if GUI.menu_screen[GUI.current_menu_screen]["buttons"][i]["text"] != None:
        tmp_fontsurf = GUI.assets.pixelfont.render(GUI.menu_screen[GUI.current_menu_screen]["buttons"][i]["text"][0], GUI.menu_screen[GUI.current_menu_screen]["buttons"][i]["text"][1], GUI.menu_screen[GUI.current_menu_screen]["buttons"][i]["text"][2])
        tmp_fontsurf = pygame.transform.scale(tmp_fontsurf, (
            (tmp_fontsurf.get_width() / tmp_fontsurf.get_height()) * (GUI.scale * 8),
            GUI.scale * 8
        ))
        GUI.surface.blit(tmp_fontsurf, (
            WIN.get_width() / 2 - (GUI.scale + GUI.assets.menu_buttons[0].get_width() * GUI.menu_screen[GUI.current_menu_screen]["starting_point"][0]) / 2 + (GUI.scale + GUI.assets.menu_buttons[0].get_width()) * GUI.menu_screen[GUI.current_menu_screen]["buttons"][i]["pos_multiplier"][0] + (GUI.menu_screen[GUI.current_menu_screen]["buttons"][i]["anim"] * 1 if GUI.menu_screen[GUI.current_menu_screen]["buttons"][i]["anim_positive"] else -1)           + GUI.assets.menu_buttons[0].get_width() / 2 - tmp_fontsurf.get_width() / 2,
            WIN.get_height() / 2 - (GUI.scale + GUI.assets.menu_buttons[0].get_height() * GUI.menu_screen[GUI.current_menu_screen]["starting_point"][1]) / 2 + (GUI.scale + GUI.assets.menu_buttons[0].get_height()) * GUI.menu_screen[GUI.current_menu_screen]["buttons"][i]["pos_multiplier"][1]                                                                                                                                                                  + 4 * GUI.scale + (GUI.scale * 2 if tmp_ispushed else 0)
        ))

    # Button A
    i = 1
    tmp_ispushed = False if GUI.menu_screen[GUI.current_menu_screen]["buttons"][i]["button_assignment"] == None else \
        controls[GUI.menu_screen[GUI.current_menu_screen]["buttons"][i]["button_push"]] and GUI.selected_button == GUI.menu_screen[GUI.current_menu_screen]["buttons"][i]["button_assignment"]
    GUI.timer += 2 if tmp_ispushed else 0
    tmp_imgs = (eval(GUI.menu_screen[GUI.current_menu_screen]["buttons"][i]["image_push"]) if tmp_ispushed else (eval(GUI.menu_screen[GUI.current_menu_screen]["buttons"][i]["image_hover"]) if GUI.selected_button == GUI.menu_screen[GUI.current_menu_screen]["buttons"][i]["button_assignment"] else eval(GUI.menu_screen[GUI.current_menu_screen]["buttons"][i]["image"])))
    GUI.surface.blit(tmp_imgs, (
        WIN.get_width() / 2 - (GUI.scale + GUI.assets.menu_buttons[0].get_width() * GUI.menu_screen[GUI.current_menu_screen]["starting_point"][0]) / 2 + (GUI.scale + GUI.assets.menu_buttons[0].get_width()) * GUI.menu_screen[GUI.current_menu_screen]["buttons"][i]["pos_multiplier"][0] + (GUI.menu_screen[GUI.current_menu_screen]["buttons"][i]["anim"] * 1 if GUI.menu_screen[GUI.current_menu_screen]["buttons"][i]["anim_positive"] else -1),
        WIN.get_height() / 2 - (GUI.scale + GUI.assets.menu_buttons[0].get_height() * GUI.menu_screen[GUI.current_menu_screen]["starting_point"][1]) / 2 + (GUI.scale + GUI.assets.menu_buttons[0].get_height()) * GUI.menu_screen[GUI.current_menu_screen]["buttons"][i]["pos_multiplier"][1]
    ))
    if GUI.menu_screen[GUI.current_menu_screen]["buttons"][i]["text"] != None:
        tmp_fontsurf = GUI.assets.pixelfont.render(GUI.menu_screen[GUI.current_menu_screen]["buttons"][i]["text"][0], GUI.menu_screen[GUI.current_menu_screen]["buttons"][i]["text"][1], GUI.menu_screen[GUI.current_menu_screen]["buttons"][i]["text"][2])
        tmp_fontsurf = pygame.transform.scale(tmp_fontsurf, (
            (tmp_fontsurf.get_width() / tmp_fontsurf.get_height()) * (GUI.scale * 8),
            GUI.scale * 8
        ))
        GUI.surface.blit(tmp_fontsurf, (
            WIN.get_width() / 2 - (GUI.scale + GUI.assets.menu_buttons[0].get_width() * GUI.menu_screen[GUI.current_menu_screen]["starting_point"][0]) / 2 + (GUI.scale + GUI.assets.menu_buttons[0].get_width()) * GUI.menu_screen[GUI.current_menu_screen]["buttons"][i]["pos_multiplier"][0] + (GUI.menu_screen[GUI.current_menu_screen]["buttons"][i]["anim"] * 1 if GUI.menu_screen[GUI.current_menu_screen]["buttons"][i]["anim_positive"] else -1)           + GUI.assets.menu_buttons[0].get_width() / 2 - tmp_fontsurf.get_width() / 2,
            WIN.get_height() / 2 - (GUI.scale + GUI.assets.menu_buttons[0].get_height() * GUI.menu_screen[GUI.current_menu_screen]["starting_point"][1]) / 2 + (GUI.scale + GUI.assets.menu_buttons[0].get_height()) * GUI.menu_screen[GUI.current_menu_screen]["buttons"][i]["pos_multiplier"][1]                                                                                                                                                                  + 4 * GUI.scale + (GUI.scale * 2 if tmp_ispushed else 0)
        ))

    # Button B
    i = 2
    tmp_ispushed = False if GUI.menu_screen[GUI.current_menu_screen]["buttons"][i]["button_assignment"] == None else \
        controls[GUI.menu_screen[GUI.current_menu_screen]["buttons"][i]["button_push"]] and GUI.selected_button == GUI.menu_screen[GUI.current_menu_screen]["buttons"][i]["button_assignment"]
    GUI.timer += 2 if tmp_ispushed else 0
    tmp_imgs = (eval(GUI.menu_screen[GUI.current_menu_screen]["buttons"][i]["image_push"]) if tmp_ispushed else (eval(GUI.menu_screen[GUI.current_menu_screen]["buttons"][i]["image_hover"]) if GUI.selected_button == GUI.menu_screen[GUI.current_menu_screen]["buttons"][i]["button_assignment"] else eval(GUI.menu_screen[GUI.current_menu_screen]["buttons"][i]["image"])))
    GUI.surface.blit(tmp_imgs, (
        WIN.get_width() / 2 - (GUI.scale + GUI.assets.menu_buttons[0].get_width() * GUI.menu_screen[GUI.current_menu_screen]["starting_point"][0]) / 2 + (GUI.scale + GUI.assets.menu_buttons[0].get_width()) * GUI.menu_screen[GUI.current_menu_screen]["buttons"][i]["pos_multiplier"][0] + (GUI.menu_screen[GUI.current_menu_screen]["buttons"][i]["anim"] * 1 if GUI.menu_screen[GUI.current_menu_screen]["buttons"][i]["anim_positive"] else -1),
        WIN.get_height() / 2 - (GUI.scale + GUI.assets.menu_buttons[0].get_height() * GUI.menu_screen[GUI.current_menu_screen]["starting_point"][1]) / 2 + (GUI.scale + GUI.assets.menu_buttons[0].get_height()) * GUI.menu_screen[GUI.current_menu_screen]["buttons"][i]["pos_multiplier"][1]
    ))
    if GUI.menu_screen[GUI.current_menu_screen]["buttons"][i]["text"] != None:
        tmp_fontsurf = GUI.assets.pixelfont.render(GUI.menu_screen[GUI.current_menu_screen]["buttons"][i]["text"][0], GUI.menu_screen[GUI.current_menu_screen]["buttons"][i]["text"][1], GUI.menu_screen[GUI.current_menu_screen]["buttons"][i]["text"][2])
        tmp_fontsurf = pygame.transform.scale(tmp_fontsurf, (
            (tmp_fontsurf.get_width() / tmp_fontsurf.get_height()) * (GUI.scale * 8),
            GUI.scale * 8
        ))
        GUI.surface.blit(tmp_fontsurf, (
            WIN.get_width() / 2 - (GUI.scale + GUI.assets.menu_buttons[0].get_width() * GUI.menu_screen[GUI.current_menu_screen]["starting_point"][0]) / 2 + (GUI.scale + GUI.assets.menu_buttons[0].get_width()) * GUI.menu_screen[GUI.current_menu_screen]["buttons"][i]["pos_multiplier"][0] + (GUI.menu_screen[GUI.current_menu_screen]["buttons"][i]["anim"] * 1 if GUI.menu_screen[GUI.current_menu_screen]["buttons"][i]["anim_positive"] else -1)           + GUI.assets.menu_buttons[0].get_width() / 2 - tmp_fontsurf.get_width() / 2,
            WIN.get_height() / 2 - (GUI.scale + GUI.assets.menu_buttons[0].get_height() * GUI.menu_screen[GUI.current_menu_screen]["starting_point"][1]) / 2 + (GUI.scale + GUI.assets.menu_buttons[0].get_height()) * GUI.menu_screen[GUI.current_menu_screen]["buttons"][i]["pos_multiplier"][1]                                                                                                                                                                  + 4 * GUI.scale + (GUI.scale * 2 if tmp_ispushed else 0)
        ))

    # Button X
    i = 3
    tmp_ispushed = False if GUI.menu_screen[GUI.current_menu_screen]["buttons"][i]["button_assignment"] == None else \
        controls[GUI.menu_screen[GUI.current_menu_screen]["buttons"][i]["button_push"]] and GUI.selected_button == GUI.menu_screen[GUI.current_menu_screen]["buttons"][i]["button_assignment"]
    GUI.timer += 2 if tmp_ispushed else 0
    tmp_imgs = (eval(GUI.menu_screen[GUI.current_menu_screen]["buttons"][i]["image_push"]) if tmp_ispushed else (eval(GUI.menu_screen[GUI.current_menu_screen]["buttons"][i]["image_hover"]) if GUI.selected_button == GUI.menu_screen[GUI.current_menu_screen]["buttons"][i]["button_assignment"] else eval(GUI.menu_screen[GUI.current_menu_screen]["buttons"][i]["image"])))
    GUI.surface.blit(tmp_imgs, (
        WIN.get_width() / 2 - (GUI.scale + GUI.assets.menu_buttons[0].get_width() * GUI.menu_screen[GUI.current_menu_screen]["starting_point"][0]) / 2 + (GUI.scale + GUI.assets.menu_buttons[0].get_width()) * GUI.menu_screen[GUI.current_menu_screen]["buttons"][i]["pos_multiplier"][0] + (GUI.menu_screen[GUI.current_menu_screen]["buttons"][i]["anim"] * 1 if GUI.menu_screen[GUI.current_menu_screen]["buttons"][i]["anim_positive"] else -1),
        WIN.get_height() / 2 - (GUI.scale + GUI.assets.menu_buttons[0].get_height() * GUI.menu_screen[GUI.current_menu_screen]["starting_point"][1]) / 2 + (GUI.scale + GUI.assets.menu_buttons[0].get_height()) * GUI.menu_screen[GUI.current_menu_screen]["buttons"][i]["pos_multiplier"][1]
    ))
    if GUI.menu_screen[GUI.current_menu_screen]["buttons"][i]["text"] != None:
        tmp_fontsurf = GUI.assets.pixelfont.render(GUI.menu_screen[GUI.current_menu_screen]["buttons"][i]["text"][0], GUI.menu_screen[GUI.current_menu_screen]["buttons"][i]["text"][1], GUI.menu_screen[GUI.current_menu_screen]["buttons"][i]["text"][2])
        tmp_fontsurf = pygame.transform.scale(tmp_fontsurf, (
            (tmp_fontsurf.get_width() / tmp_fontsurf.get_height()) * (GUI.scale * 8),
            GUI.scale * 8
        ))
        GUI.surface.blit(tmp_fontsurf, (
            WIN.get_width() / 2 - (GUI.scale + GUI.assets.menu_buttons[0].get_width() * GUI.menu_screen[GUI.current_menu_screen]["starting_point"][0]) / 2 + (GUI.scale + GUI.assets.menu_buttons[0].get_width()) * GUI.menu_screen[GUI.current_menu_screen]["buttons"][i]["pos_multiplier"][0] + (GUI.menu_screen[GUI.current_menu_screen]["buttons"][i]["anim"] * 1 if GUI.menu_screen[GUI.current_menu_screen]["buttons"][i]["anim_positive"] else -1)           + GUI.assets.menu_buttons[0].get_width() / 2 - tmp_fontsurf.get_width() / 2,
            WIN.get_height() / 2 - (GUI.scale + GUI.assets.menu_buttons[0].get_height() * GUI.menu_screen[GUI.current_menu_screen]["starting_point"][1]) / 2 + (GUI.scale + GUI.assets.menu_buttons[0].get_height()) * GUI.menu_screen[GUI.current_menu_screen]["buttons"][i]["pos_multiplier"][1]                                                                                                                                                                  + 4 * GUI.scale + (GUI.scale * 2 if tmp_ispushed else 0)
        ))

    # Button Y
    i = 4
    tmp_ispushed = False if GUI.menu_screen[GUI.current_menu_screen]["buttons"][i]["button_assignment"] == None else \
        controls[GUI.menu_screen[GUI.current_menu_screen]["buttons"][i]["button_push"]] and GUI.selected_button == GUI.menu_screen[GUI.current_menu_screen]["buttons"][i]["button_assignment"]
    GUI.timer += 2 if tmp_ispushed else 0
    tmp_imgs = (eval(GUI.menu_screen[GUI.current_menu_screen]["buttons"][i]["image_push"]) if tmp_ispushed else (eval(GUI.menu_screen[GUI.current_menu_screen]["buttons"][i]["image_hover"]) if GUI.selected_button == GUI.menu_screen[GUI.current_menu_screen]["buttons"][i]["button_assignment"] else eval(GUI.menu_screen[GUI.current_menu_screen]["buttons"][i]["image"])))
    GUI.surface.blit(tmp_imgs, (
        WIN.get_width() / 2 - (GUI.scale + GUI.assets.menu_buttons[0].get_width() * GUI.menu_screen[GUI.current_menu_screen]["starting_point"][0]) / 2 + (GUI.scale + GUI.assets.menu_buttons[0].get_width()) * GUI.menu_screen[GUI.current_menu_screen]["buttons"][i]["pos_multiplier"][0] + (GUI.menu_screen[GUI.current_menu_screen]["buttons"][i]["anim"] * 1 if GUI.menu_screen[GUI.current_menu_screen]["buttons"][i]["anim_positive"] else -1),
        WIN.get_height() / 2 - (GUI.scale + GUI.assets.menu_buttons[0].get_height() * GUI.menu_screen[GUI.current_menu_screen]["starting_point"][1]) / 2 + (GUI.scale + GUI.assets.menu_buttons[0].get_height()) * GUI.menu_screen[GUI.current_menu_screen]["buttons"][i]["pos_multiplier"][1]
    ))
    if GUI.menu_screen[GUI.current_menu_screen]["buttons"][i]["text"] != None:
        tmp_fontsurf = GUI.assets.pixelfont.render(GUI.menu_screen[GUI.current_menu_screen]["buttons"][i]["text"][0], GUI.menu_screen[GUI.current_menu_screen]["buttons"][i]["text"][1], GUI.menu_screen[GUI.current_menu_screen]["buttons"][i]["text"][2])
        tmp_fontsurf = pygame.transform.scale(tmp_fontsurf, (
            (tmp_fontsurf.get_width() / tmp_fontsurf.get_height()) * (GUI.scale * 8),
            GUI.scale * 8
        ))
        GUI.surface.blit(tmp_fontsurf, (
            WIN.get_width() / 2 - (GUI.scale + GUI.assets.menu_buttons[0].get_width() * GUI.menu_screen[GUI.current_menu_screen]["starting_point"][0]) / 2 + (GUI.scale + GUI.assets.menu_buttons[0].get_width()) * GUI.menu_screen[GUI.current_menu_screen]["buttons"][i]["pos_multiplier"][0] + (GUI.menu_screen[GUI.current_menu_screen]["buttons"][i]["anim"] * 1 if GUI.menu_screen[GUI.current_menu_screen]["buttons"][i]["anim_positive"] else -1)           + GUI.assets.menu_buttons[0].get_width() / 2 - tmp_fontsurf.get_width() / 2,
            WIN.get_height() / 2 - (GUI.scale + GUI.assets.menu_buttons[0].get_height() * GUI.menu_screen[GUI.current_menu_screen]["starting_point"][1]) / 2 + (GUI.scale + GUI.assets.menu_buttons[0].get_height()) * GUI.menu_screen[GUI.current_menu_screen]["buttons"][i]["pos_multiplier"][1]                                                                                                                                                                  + 4 * GUI.scale + (GUI.scale * 2 if tmp_ispushed else 0)
        ))

    GUI.timer -= 1

    GUI.timer = max(0, min(GUI.timer, 50))

    GUI.anim[0] /= 1.05

    if GUI.time_passed > 20: GUI.anim[1] /= 1.05
    if GUI.time_passed > 40: GUI.anim[2] /= 1.05

    pygame.draw.rect(GUI.surface, (0, 255, 0), pygame.Rect(
        0,
        WIN.get_height() - GUI.scale,
        (WIN.get_width() / 50) * GUI.timer,
        GUI.scale
    ))
    WIN.blit(GUI.surface, (0, 0))
    
    GUI.surface = pygame.Surface(WIN.get_size())

    #print(GUI.controls_previously_pressed)

print(str(time.time_ns()) + " Done")