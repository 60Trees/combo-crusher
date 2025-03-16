import random
import sys
import time

import config as CONFIG
import input_ID as INP
import pygame
import util_handling

button_names = [
    "Move Left",
    "Move Right",
    "Jump",
    "Roll",
    "Dodge",
    "Inventory",
    "Selected Item Left",
    "Selected Item Right",
    "Attack toggle",
    "Ranged toggle",
    "Pause",
    "Minimap",
    "Gui Left",
    "Gui Right",
    "Gui Up",
    "Gui Down",
    "A",
    "B",
    "X",
    "Y",
    "Sneak"
]


joystick_names = [
    "Left stick left/right",
    "Left stick up/down",
    "Right stick left/right",
    "Right stick up/down",
    "Left trigger/LT",
    "Right trigger/RT",
    "D-Pad/JoyHat Left/Right",
    "D-Pad/JoyHat Up/Down",
]

BtnNmsToGmInp = {
    "Move Left": INP.moveleft,
    "Move Right": INP.moveright,
    "Jump": INP.jump,
    "Roll": INP.roll,
    "Dodge": INP.dodge,
    "Inventory": INP.inventory,
    "Selected Item Left": INP.item_left,
    "Selected Item Right": INP.item_right,
    "Attack toggle": INP.Tgl_attack_toggle,
    "Ranged toggle": INP.Tgl_range_toggle,
    "Pause": INP.pausegame,
    "Minimap": INP.minimap,
    "Gui Left": INP.GUI_Left,
    "Gui Right": INP.GUI_Right,
    "Gui Up": INP.GUI_Up,
    "Gui Down": INP.GUI_Down,
    "A": INP.GUI_A,
    "B": INP.GUI_B,
    "X": INP.GUI_X,
    "Y": INP.GUI_Y,
    "Sneak": INP.sneak
}

def btn_name_to_inp(btn_name):
    tmp = BtnNmsToGmInp[btn_name]
    return tmp

INP_count = len([attr for attr in vars(INP) if not attr.startswith("__")])

class Active_controls:
    windowResized = False
    pushed = []
    tapped = []
    
    for i in range(INP_count):
        pushed.append(False)

    class Cursor:
        pos = (0, 0)
        scroll = 0
        hasMoved = False
        class Click:
            hold = [False, False, False]
            click = [False, False, False]
        click = Click()
        
        isHidden = False
    
    cursor = Cursor

settings = {}

# Initialize the joystick
pygame.joystick.init()

try:
    settings = util_handling.load('main/settings.json')

    # Loads part of the settings JSON to ensure it is proper.
    settings["control_layout"]
except IOError as e:
    print(f"Error occured while loading: {e}")
    if not input("controller_settings.json does not exist or is corrupt. Continue: Y / N -->").lower() == "y":
        print("Force quitting...")
        sys.exit()
    settings = {
        "control_layout": {}
    }

# Check for joystick
if pygame.joystick.get_count() == 0:
    print("No joystick detected")
    controller_name = "keyboard"
    isNewController = controller_name not in settings["control_layout"]
    if isNewController:
        isConfiguringController = True
    else:
        isConfiguringController = False
        isConfiguringController = CONFIG.isConfiguringController
        if CONFIG.askToConfigureController:
            isConfiguringController = input(f"Do you want to change controller configuration for {controller_name}? Y = yes, not y = no? -->").lower() == "y"
    if isConfiguringController:
        pygame.init()
        TMP_WIN = pygame.display.set_mode((200, 200))

        settings["control_layout"][controller_name] = {}
        settings["control_layout"][controller_name]["action_specific"] = {}
        layout_path = settings["control_layout"][controller_name]

        for i in range(len(button_names)):
            def listitems(lst):
                return ''.join([x + ((", " if x != lst[-2] else " and ") if x != lst[-1] else "") for x in lst])
            print(f"Controls concist of {listitems(button_names)}.")
            print(f"Bind action to {button_names[i]}:")

            confirmed_button = None

            while confirmed_button is None:
                for event in pygame.event.get():
                    if event.type == pygame.KEYDOWN:
                        confirmed_button = event.key
                        layout_path["action_specific"][button_names[i]] = {
                            "isButton": True,
                            "id": confirmed_button,
                            "axisValue": None
                        }
                        print(f"Keyboard key {event.key} pressed.")
else:
    # Use the first joystick
    supported_controllers = [
        "Xbox Series X Controller"
    ]
    
    joystick = pygame.joystick.Joystick(0)
    joystick.init()
    controller_name = joystick.get_name()
    print(f"Controller {controller_name} detected!")
    if controller_name not in supported_controllers:
        if input("Continue code without supported controllers? Y for yes (Experimental, might break!!!) --> ").lower() != "y":
            print("Exiting code...")
            sys.exit()

    isNewController = controller_name not in settings["control_layout"]
    temp = ("" if isNewController else "n\'t")
    print(f'{controller_name} has{temp} been used before.')
    if isNewController:
        isConfiguringController = CONFIG.isConfiguringController
        if CONFIG.askToConfigureController:
            isConfiguringController = input(f"Do you want to change controller configuration for {controller_name}? Y = yes, not y = no? -->").lower() == "y"
    else:
        isConfiguringController = CONFIG.isConfiguringController
        #isConfiguringController =input(f"Do you want to change controller configuration for {controller_name}? Y = yes, not y = no? -->").lower() == "y"
    if isConfiguringController:

        pygame.init()
        TMP_WIN = pygame.display.set_mode((200, 200))

        settings["control_layout"][controller_name] = {}
        settings["control_layout"][controller_name]["action_specific"] = {}
        layout_path = settings["control_layout"][controller_name]


        for i in range(len(button_names)):
            def listitems(lst):
                return ''.join([x + ((", " if x != lst[-2] else " and ") if x != lst[-1] else "") for x in lst])
            print(f"Controls concist of {listitems(button_names)}.")
            print(f"Bind action to {button_names[i]}:")

            previously_pushed_button = None
            confirmed_button = None
            confirmed_axis = None
            confirmed_axis_value = None
            previously_pushed_axis = None
            previously_pushed_axis_value = None

            while confirmed_button is None and confirmed_axis is None:
                for event in pygame.event.get():
                    if event.type == pygame.JOYAXISMOTION:
                        if event.value < -0.8 or event.value > 0.8 and (not (event.axis == 4 or event.axis == 5)):
                            print(f"Axis {event.axis} or {joystick_names[event.axis]} value: {event.value}")
                            if previously_pushed_axis == event.axis and previously_pushed_axis_value == round(event.value):
                                confirmed_axis = event.axis
                                confirmed_axis_value = round(event.value)
                                joystick.rumble(1, 1, 1000)
                                layout_path["action_specific"][button_names[i]] = {
                                    "isButton": False,
                                    "id": confirmed_axis,
                                    "axisValue": confirmed_axis_value
                                }
                                print("Wait...")
                                time.sleep(0.5)
                                pygame.event.get()
                                print("Confirmed!!")
                            else:
                                previously_pushed_axis = event.axis
                                previously_pushed_axis_value = round(event.value)
                                confirmed_button = None
                                print("Wait...")
                                time.sleep(0.5)
                                pygame.event.get()
                                print("Do again to confirm")
                        elif event.axis == 4 or event.axis == 5 and event.value > 0.8:
                            print(f"Triggers pressed, id={event.axis}, value={round(event.value*100)/100}")
                            if previously_pushed_axis == event.axis:
                                confirmed_axis = event.axis
                                confirmed_axis_value = 1
                                joystick.rumble(1, 1, 1000)
                                layout_path["action_specific"][button_names[i]] = {
                                    "isButton": False,
                                    "id": confirmed_axis,
                                    "axisValue": 1
                                }
                                print("Wait...")
                                time.sleep(0.5)
                                pygame.event.get()
                                print("Confirmed!!")
                            else:
                                previously_pushed_axis_value = 1
                                previously_pushed_axis = event.axis
                                confirmed_button = None

                                print("Wait...")
                                time.sleep(0.5)
                                pygame.event.get()
                                print("Do again to confirm")

                    if event.type == pygame.JOYHATMOTION:
                            print(f"Hat: {event.value}")
                            if event.value != (0, 0):
                                print(f"Axis {(6 if event.value[0] != 0 else 7)} or {joystick_names[6 if event.value[0] != 0 else 7]} value: {event.value[0 if event.value[0] != 0 else 1]}")
                                if previously_pushed_axis == (6 if event.value[0] != 0 else 7) and previously_pushed_axis_value == round(event.value[0] if event.value[0] != 0 else event.value[1]):
                                    confirmed_axis = (6 if event.value[0] != 0 else 7)
                                    confirmed_axis_value = round(event.value[0] if event.value[0] != 0 else event.value[1])
                                    joystick.rumble(1, 1, 1000)
                                    layout_path["action_specific"][button_names[i]] = {
                                        "isButton": False,
                                        "id": confirmed_axis,
                                        "axisValue": confirmed_axis_value
                                    }
                                    print("Wait...")
                                    time.sleep(0.5)
                                    pygame.event.get()
                                    print("Confirmed!!")
                                else:
                                    confirmed_button = None
                                    previously_pushed_axis_value = round(event.value[0] if event.value[0] != 0 else event.value[1])
                                    
                                    print("Wait...")
                                    time.sleep(0.5)
                                    pygame.event.get()
                                    print("Do again to confirm")

                    elif event.type == pygame.JOYBUTTONDOWN:
                        print(f"Button {event.button} pressed")

                        if previously_pushed_button == event.button:
                            confirmed_button = event.button
                            joystick.rumble(1, 1, 1000)
                            layout_path["action_specific"][button_names[i]] = {
                                "isButton": True,
                                "id": confirmed_button,
                                "axisValue": None
                            }
                            print("Wait...")
                            time.sleep(0.5)
                            pygame.event.get()
                            print("Confirmed!")
                        else:
                            previously_pushed_button = event.button
                            confirmed_axis = None
                            confirmed_axis_value = None
                            
                            print("Wait...")
                            time.sleep(0.5)
                            pygame.event.get()
                            print("Do again to confirm")

                    elif event.type == pygame.JOYBUTTONUP:
                        print(f"Button {event.button} released")

        settings["control_layout"][controller_name] = layout_path

result = {"buttons": {}, "joysticks": {}}

for action, props in settings["control_layout"][controller_name]["action_specific"].items():
    if props["isButton"]:
        if str(props["id"]) not in result["buttons"]:
            result["buttons"][str(props["id"])] = []

        result["buttons"][str(props["id"])].append(action)
    else:
        joystick_id = str(props["id"])

        if joystick_id not in result["joysticks"]:
            result["joysticks"][joystick_id] = {}

        if str(props["axisValue"]) not in result["joysticks"][joystick_id]:
            result["joysticks"][joystick_id][str(props["axisValue"])] = []

        result["joysticks"][joystick_id][str(props["axisValue"])].append(action)

settings["control_layout"][controller_name]["button_specific"] = result["buttons"]
settings["control_layout"][controller_name]["joystick_specific"] = result["joysticks"]

util_handling.dump(settings, 'main/settings.json')

def String_to_control(string, CTRL: Active_controls):
    return BtnNmsToGmInp[string]

def register_input(event, CTRL: Active_controls):
    # ======================================================================================================================== #
    #                                              JOYSTICK OR AXIS MOTION                                                     #
    # ======================================================================================================================== #
    if event.type == pygame.JOYAXISMOTION:
        # ==================================================================================================================== #
        #                                                AXIS MOTION                                                           #
        # ==================================================================================================================== #
        if event.axis == 4 or event.axis == 5:
            if event.value > -0.8:
                CTRL.cursor.isHidden = True
                if str(event.axis) in settings["control_layout"][controller_name]["joystick_specific"]:
                    try:
                        tmp = settings["control_layout"][controller_name]["joystick_specific"][str(event.axis)]["1"]
                        for i in tmp:
                            if String_to_control(i, CTRL) is False:
                                joystick.rumble(random.randint(1,3)/9,(random.randint(1,3)-1)/9,random.randint(10,20)*5)

                            CTRL.pushed[String_to_control(i, CTRL)] = True
                            CTRL.tapped[String_to_control(i, CTRL)] = True
                    except KeyError:
                        pass
                    
            elif str(event.axis) in settings["control_layout"][controller_name]["joystick_specific"]:
                CTRL.cursor.isHidden = True
                try:
                    tmp = settings["control_layout"][controller_name]["joystick_specific"][str(event.axis)]["1"]
                    for i in tmp:
                        CTRL.pushed[String_to_control(i, CTRL)] = False
                except KeyError:
                    pass
                
        elif event.value > 0.5 or event.value < -0.5:
            if str(event.axis) in settings["control_layout"][controller_name]["joystick_specific"]:
                if str(event.value)[0] == "-" and "-1" in settings["control_layout"][controller_name]["joystick_specific"][str(event.axis)]:
                    
                    tmp = settings["control_layout"][controller_name]["joystick_specific"][str(event.axis)]["-1"]
                    
                    for i in tmp:
                        CTRL.pushed[String_to_control(i, CTRL)] = True
                        CTRL.tapped[String_to_control(i, CTRL)] = not CTRL.tapped[String_to_control(i, CTRL)]

                    tmp = settings["control_layout"][controller_name]["joystick_specific"][str(event.axis)]["1"]
                    
                    for i in tmp:
                        CTRL.pushed[String_to_control(i, CTRL)] = False

                elif str(event.value)[0] != "-":
                    tmp = settings["control_layout"][controller_name]["joystick_specific"][str(event.axis)]["1"]
                    
                    for i in tmp:
                        CTRL.pushed[String_to_control(i, CTRL)] = True
                        CTRL.tapped[String_to_control(i, CTRL)] = not CTRL.tapped[String_to_control(i, CTRL)]

                    tmp = settings["control_layout"][controller_name]["joystick_specific"][str(event.axis)]["-1"]
                    
                    for i in tmp:
                        CTRL.pushed[String_to_control(i, CTRL)] = False
        else:
            if str(event.axis) in settings["control_layout"][controller_name]["joystick_specific"]:
                if str(event.value)[0] == "-" and "-1" in settings["control_layout"][controller_name]["joystick_specific"][str(event.axis)]:
                    tmp = settings["control_layout"][controller_name]["joystick_specific"][str(event.axis)]["-1"]
                    
                    for i in tmp:
                        CTRL.pushed[String_to_control(i, CTRL)] = False
                elif str(event.value)[0] != "-":
                    tmp = settings["control_layout"][controller_name]["joystick_specific"][str(event.axis)]["1"]
                    
                    for i in tmp:
                        CTRL.pushed[String_to_control(i, CTRL)] = False
    # ======================================================================================================================== #
    #                                                   BUTTON PUSH                                                            #
    # ======================================================================================================================== #
    elif event.type == pygame.JOYBUTTONDOWN:
        if str(event.button) in settings["control_layout"][controller_name]["button_specific"]:
            tmp = settings["control_layout"][controller_name]["button_specific"][str(event.button)]
            for i in tmp:
                CTRL.pushed[String_to_control(i, CTRL)] = True
                CTRL.tapped[String_to_control(i, CTRL)] = True
            joystick.rumble(random.randint(1, 3) / 9, (random.randint(1, 3) - 1) / 9, random.randint(10, 20) * 5)
        CTRL.cursor.isHidden = True

    elif event.type == pygame.JOYBUTTONUP:
        if str(event.button) in settings["control_layout"][controller_name]["button_specific"]:
            tmp = settings["control_layout"][controller_name]["button_specific"][str(event.button)]
            for i in tmp:
                CTRL.pushed[String_to_control(i, CTRL)] = False
            joystick.rumble(random.randint(1, 3) / 9, (random.randint(1, 3) - 1) / 9, random.randint(10, 20) * 5)
        CTRL.cursor.isHidden = True

    elif event.type == pygame.KEYDOWN:
        if str(event.key) in settings["control_layout"][controller_name]["button_specific"]:
            tmp = settings["control_layout"][controller_name]["button_specific"][str(event.key)]
            for i in tmp:
                CTRL.pushed[String_to_control(i, CTRL)] = True
                CTRL.tapped[String_to_control(i, CTRL)] = True
        CTRL.cursor.isHidden = True

    elif event.type == pygame.KEYUP:
        if str(event.key) in settings["control_layout"][controller_name]["button_specific"]:
            tmp = settings["control_layout"][controller_name]["button_specific"][str(event.key)]
            for i in tmp:
                CTRL.pushed[String_to_control(i, CTRL)] = False
        CTRL.cursor.isHidden = True
    
    elif event.type == pygame.MOUSEMOTION:
        CTRL.cursor.hasMoved = True
        CTRL.cursor.pos = event.pos

    elif event.type == pygame.MOUSEBUTTONDOWN and event.button not in (pygame.BUTTON_WHEELDOWN, pygame.BUTTON_WHEELUP):
        CTRL.cursor.click.click[event.button - 1] = True
    elif event.type == pygame.WINDOWRESIZED:
        CTRL.windowResized = True

def update_input(event, CTRL: Active_controls):
    register_input(event, CTRL)


def prepare_input(CTRL: Active_controls):
    # This is run before update_input

    CTRL.cursor.click.hold = pygame.mouse.get_pressed()

    CTRL.windowResized = False
    CTRL.tapped = []
    for i in range(len([attr for attr in vars(INP) if not attr.startswith("__")])):
        CTRL.tapped.append(False)

    CTRL.cursor.hasMoved = False
    CTRL.cursor.click.click = [False, False, False]

def reset_input(CTRL: Active_controls):
    # This is run after update_input
    if CTRL.cursor.hasMoved:
        CTRL.cursor.isHidden = False