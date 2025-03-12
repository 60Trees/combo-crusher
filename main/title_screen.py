import input_ID as INP
import pygame
import title_screen_layout

pygame.font.init()

menu_title = pygame.image.load("main/assets/gui/title.png")

class class_GUI():
    def __init__(self):
        self.timer = 0
        self.timer_maximum = 15
        self.current_menu_screen = "main_menu"
        self.menu_screen = title_screen_layout.layout
        self.selected_button = 0
        self.selected_button_maximum = self.menu_screen[self.current_menu_screen]["max_buttons"]
        self.anim = [
            3.000, 3.000, 3.000
        ]
        self.scale = 5

        class Assets():
            def __init__(self):
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
        self.assets = Assets()
        self.time_passed = 0
    def reset_anim(self, WIN):
        print("Resetting anim!!")
        self.anim[0] = 3.000
        self.anim[1] = 3.000
        self.anim[2] = 3.000
        self.time_passed  = 0
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

def draw_menu_screen(data, WIN):
    print(GUI.anim)
    GUI.time_passed += 1
    
    if data.GMCTRL.tapped[INP.GUI_Up]:
        if GUI.selected_button is not None:
            GUI.selected_button -= 1
        else:
            GUI.selected_button = 0

    if data.GMCTRL.tapped[INP.GUI_Down]:
        if GUI.selected_button is not None:
            GUI.selected_button += 1
        else:
            GUI.selected_button = 0

    if data.GMCTRL.tapped[INP.GUI_Left] or data.GMCTRL.tapped[INP.item_left]:
        if GUI.selected_button is not None:
            GUI.selected_button -= 2
        else:
            GUI.selected_button = 0

    if data.GMCTRL.tapped[INP.GUI_Right] or data.GMCTRL.tapped[INP.item_right]:
        if GUI.selected_button is not None:
            GUI.selected_button += 2
        else:
            GUI.selected_button = 0
    
        while GUI.selected_button > GUI.selected_button_maximum:
            GUI.selected_button -= GUI.selected_button_maximum + 1
        while GUI.selected_button < 0:
            GUI.selected_button += GUI.selected_button_maximum + 1

    future_menu_screen = None

    timer_goesup = False

    if data.GMCTRL.cursor.hasMoved:
        GUI.selected_button = None

    for i in range(len(GUI.menu_screen[GUI.current_menu_screen]["buttons"])):
        current_button = GUI.menu_screen[GUI.current_menu_screen]["buttons"][i]
        
        # This is where the button will be drawn
        button_positionX = WIN.get_width() / 2 - (GUI.scale + GUI.assets.menu_buttons[0].get_width() * GUI.menu_screen[GUI.current_menu_screen]["starting_point"][0]) / 2 + (GUI.scale + GUI.assets.menu_buttons[0].get_width()) * current_button["pos_multiplier"][0]
        button_positionX += (GUI.anim[current_button["anim"]] * (WIN.get_width() if current_button["anim_positive"] else -WIN.get_width()))

        button_positionY = WIN.get_height() / 2 - (GUI.scale + GUI.assets.menu_buttons[0].get_height() * GUI.menu_screen[GUI.current_menu_screen]["starting_point"][1]) / 2 + (GUI.scale + GUI.assets.menu_buttons[0].get_height()) * current_button["pos_multiplier"][1]
        
        if current_button["button_assignment"] is not None and pygame.Rect(button_positionX, button_positionY, GUI.assets.menu_buttons[0].get_width(), GUI.assets.menu_buttons[0].get_height()).collidepoint(data.GMCTRL.cursor.pos):
            GUI.selected_button = current_button["button_assignment"]

        tmp_ispushed = \
            (data.GMCTRL.pushed[current_button["button_push"]] or (data.GMCTRL.cursor.click.hold[0] and GUI.selected_button == current_button["button_assignment"])) \
                if current_button["button_push"] is not None else \
            ((data.GMCTRL.pushed[INP.GUI_A] or data.GMCTRL.cursor.click.hold[0]) and GUI.selected_button == current_button["button_assignment"])

        if current_button["button_assignment"] is None:
            tmp_ispushed = False

        if False if current_button["button_push"] is None else data.GMCTRL.pushed[current_button["button_push"]]:
            GUI.selected_button = current_button["button_assignment"]
        if tmp_ispushed:
            timer_goesup = True
            if GUI.timer >= GUI.timer_maximum:
                future_menu_screen = current_button["button_push_menu_screen"]
                print(current_button["button_push_menu_screen"])
                GUI.timer = 0
        
        tmp_imgs = None
        if current_button["image_push"] is not None and current_button["image_hover"] is not None:
            if current_button["image"] is not None:
                tmp_imgs = (eval(current_button["image_push"]) if tmp_ispushed else (eval(current_button["image_hover"]) if GUI.selected_button == current_button["button_assignment"] else eval(current_button["image"])))
        elif current_button["image"] is not None:
            tmp_imgs = eval(current_button["image"])

        if tmp_imgs is not None:
            WIN.blit(tmp_imgs, (
                button_positionX,
                button_positionY
            ))

        # Draws the text on the button (if it has text)
        if current_button["text"] is not None:
            tmp_fontsurf = GUI.assets.pixelfont.render(current_button["text"][0], current_button["text"][1], current_button["text"][2])
            tmp_fontsurf = pygame.transform.scale(tmp_fontsurf, (
                (tmp_fontsurf.get_width() / tmp_fontsurf.get_height()) * (GUI.scale * 8),
                GUI.scale * 8
            ))
            WIN.blit(tmp_fontsurf, (
                button_positionX + GUI.assets.menu_buttons[0].get_width() / 2 - tmp_fontsurf.get_width() / 2,
                button_positionY + 4 * GUI.scale + (GUI.scale * 2 if tmp_ispushed else 0)
            ))

    if future_menu_screen is not None:
        GUI.current_menu_screen = future_menu_screen
        if GUI.current_menu_screen in GUI.menu_screen:
            GUI.selected_button_maximum = GUI.menu_screen[GUI.current_menu_screen]["max_buttons"]

    if timer_goesup:
        GUI.timer += 1
    else:
        GUI.timer /= 1.1
        GUI.timer -= 1

    GUI.timer = max(0, min(GUI.timer, GUI.timer_maximum))

    if WIN.get_width() * GUI.anim[0] > 1:
        GUI.anim[0] /= 1.05
    else:
        GUI.anim[0] = 0

    if GUI.time_passed > 20:
        if WIN.get_width() * GUI.anim[1] > 1:
            GUI.anim[1] /= 1.05
        else:
            GUI.anim[1] = 0
    if GUI.time_passed > 40:
        if WIN.get_width() * GUI.anim[2] > 1:
            GUI.anim[2] /= 1.05
        else:
            GUI.anim[2] = 0

    if GUI.current_menu_screen in GUI.menu_screen:
        pygame.draw.rect(WIN, (0, 255, 0), pygame.Rect(
            0,
            WIN.get_height() - GUI.scale,
            (WIN.get_width() / GUI.timer_maximum) * GUI.timer,
            GUI.scale
        ))