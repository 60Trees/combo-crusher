import pygame
import sys
import time
import random

import json_func
import INP

print(str(time.time_ns()) + " Initialising controller.py")

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

GMCTRL = []

for i in range(INP_count):
    GMCTRL.append(False)

def get_pressed(x):
    return GMCTRL[x]

settings = {}

# Initialize the joystick
pygame.joystick.init()

try:
    settings = json_func.load('main/settings.json')

    # Loads part of the settings JSON to ensure it is proper.
    settings["control_layout"]
except:
    print("controller_settings.json does not exist or is corrupt. Writing settings file now.")
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
        isConfiguringController =input(f"Do you want to change controller configuration for {controller_name}? Y = yes, not y = no? -->").lower() == "y"
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
        isConfiguringController = True
    else:
        isConfiguringController = False
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
        
        print(str(time.time_ns()) + " Done configuring")
    print(str(time.time_ns()) + " Done checking")
print(str(time.time_ns()) + " Done init")

print(str(time.time_ns()) + " Adding button-specific layout to settings...")
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
print(str(time.time_ns()) + " Done")

print(str(time.time_ns()) + " Dumping settings config from cache...")
json_func.dump(settings, 'main/settings.json')
print(str(time.time_ns()) + " Done")

def String_to_control(string):
    if  string == "A" or \
        string == "B" or \
        string == "X" or \
        string == "Y":
        if  GMCTRL[INP.Tgl_attack_toggle] and \
            not GMCTRL[INP.Tgl_range_toggle]:
            return eval("INP.Att_attack"+string)
        elif  GMCTRL[INP.Tgl_range_toggle] and \
            not GMCTRL[INP.Tgl_attack_toggle]:
            return eval("INP.Rng_attack"+string)
        elif GMCTRL[INP.Tgl_range_toggle] and GMCTRL[INP.Tgl_attack_toggle]:
            return eval("INP.Spe_attack"+string)
        else:
            return BtnNmsToGmInp[string]
    else:
        return BtnNmsToGmInp[string]

def update_input(event):
    if event.type == pygame.JOYAXISMOTION:
        # If it's a trigger...
        if event.axis == 4 or event.axis == 5:
            # If it's pushed enough...
            if event.value > -0.8:
                if str(event.axis) in settings["control_layout"][controller_name]["joystick_specific"]:
                    tmp = settings["control_layout"][controller_name]["joystick_specific"][str(event.axis)]["1"]
                    #print(f"Trigger {tmp} pressed with {round((event.value+1)/2*100)}% force.")

                    for i in tmp:
                        if String_to_control(i) is False:
                            joystick.rumble(random.randint(1,3)/9,(random.randint(1,3)-1)/9,random.randint(10,20)*5)
                        GMCTRL[String_to_control(i)] = True
                    
            # If it's not pushed...
            elif str(event.axis) in settings["control_layout"][controller_name]["joystick_specific"]:
                tmp = settings["control_layout"][controller_name]["joystick_specific"][str(event.axis)]["1"]
                
                #print(f"Trigger {tmp} pressed with {round((event.value+1)/2*100)}% force.")

                for i in tmp:
                    GMCTRL[String_to_control(i)] = False
                
        elif event.value > 0.5 or event.value < -0.5:
            if str(event.axis) in settings["control_layout"][controller_name]["joystick_specific"]:
                if str(event.value)[0] == "-" and "-1" in settings["control_layout"][controller_name]["joystick_specific"][str(event.axis)]:
                    
                    tmp = settings["control_layout"][controller_name]["joystick_specific"][str(event.axis)]["-1"]
                    
                    for i in tmp:
                        GMCTRL[String_to_control(i)] = True

                    #print(f"Action {tmp} done.")
                    tmp = settings["control_layout"][controller_name]["joystick_specific"][str(event.axis)]["1"]
                    
                    for i in tmp:
                        GMCTRL[String_to_control(i)] = False

                    #print(f"Action {tmp} not done.")
                elif str(event.value)[0] != "-":
                    tmp = settings["control_layout"][controller_name]["joystick_specific"][str(event.axis)]["1"]
                    
                    for i in tmp:
                        GMCTRL[String_to_control(i)] = True

                    #print(f"Action {tmp} done.")
                    tmp = settings["control_layout"][controller_name]["joystick_specific"][str(event.axis)]["-1"]
                    
                    for i in tmp:
                        GMCTRL[String_to_control(i)] = False

                    #print(f"Action {tmp} not done.")
        else:
            if str(event.axis) in settings["control_layout"][controller_name]["joystick_specific"]:
                if str(event.value)[0] == "-" and "-1" in settings["control_layout"][controller_name]["joystick_specific"][str(event.axis)]:
                    tmp = settings["control_layout"][controller_name]["joystick_specific"][str(event.axis)]["-1"]
                    
                    for i in tmp:
                        GMCTRL[String_to_control(i)] = False

                    #print(f"Action {tmp} not done.")
                elif str(event.value)[0] != "-":
                    tmp = settings["control_layout"][controller_name]["joystick_specific"][str(event.axis)]["1"]
                    
                    for i in tmp:
                        GMCTRL[String_to_control(i)] = False

                    #print(f"Action {tmp} done.")
    elif event.type == pygame.JOYBUTTONDOWN:
        
        if str(event.button) in settings["control_layout"][controller_name]["button_specific"]:
            tmp = settings["control_layout"][controller_name]["button_specific"][str(event.button)]
            #print(f"Button {tmp} pressed.")
            for i in tmp:
                GMCTRL[String_to_control(i)] = True
            joystick.rumble(random.randint(1, 3) / 9, (random.randint(1, 3) - 1) / 9, random.randint(10, 20) * 5)
    elif event.type == pygame.JOYBUTTONUP:
        if str(event.button) in settings["control_layout"][controller_name]["button_specific"]:
            tmp = settings["control_layout"][controller_name]["button_specific"][str(event.button)]
            #print(f"Button {tmp} unpressed.")
            for i in tmp:
                GMCTRL[String_to_control(i)] = False
            joystick.rumble(random.randint(1, 3) / 9, (random.randint(1, 3) - 1) / 9, random.randint(10, 20) * 5)
    elif event.type == pygame.KEYDOWN:
        if str(event.key) in settings["control_layout"][controller_name]["button_specific"]:
            tmp = settings["control_layout"][controller_name]["button_specific"][str(event.key)]
            print(f"Keys {tmp} pressed.")
            for i in tmp:
                GMCTRL[String_to_control(i)] = True
    elif event.type == pygame.KEYUP:
        if str(event.key) in settings["control_layout"][controller_name]["button_specific"]:
            tmp = settings["control_layout"][controller_name]["button_specific"][str(event.key)]
            print(f"Keys {tmp} pressed.")
            for i in tmp:
                GMCTRL[String_to_control(i)] = False
                
print(str(time.time_ns()) + " Done config")

def check_input():
    check_input2()
    check_input2()

def check_input2():
    if (GMCTRL[INP.Att_attackX] or \
        GMCTRL[INP.Att_attackY] or \
        GMCTRL[INP.Att_attackB] or \
        GMCTRL[INP.Att_attackA]) and ( \
        GMCTRL[INP.Tgl_range_toggle] or (
        not GMCTRL[INP.Tgl_attack_toggle]
        )):
        GMCTRL[INP.Att_attackX] = False
        GMCTRL[INP.Att_attackY] = False
        GMCTRL[INP.Att_attackB] = False
        GMCTRL[INP.Att_attackA] = False

    if (GMCTRL[INP.Rng_attackX] or \
        GMCTRL[INP.Rng_attackY] or \
        GMCTRL[INP.Rng_attackB] or \
        GMCTRL[INP.Rng_attackA]) and ( \
        GMCTRL[INP.Tgl_attack_toggle] or (
        not GMCTRL[INP.Tgl_range_toggle]
        )):
        GMCTRL[INP.Rng_attackX] = False
        GMCTRL[INP.Rng_attackY] = False
        GMCTRL[INP.Rng_attackB] = False
        GMCTRL[INP.Rng_attackA] = False

    if (GMCTRL[INP.Spe_attackX] or \
        GMCTRL[INP.Spe_attackY] or \
        GMCTRL[INP.Spe_attackB] or \
        GMCTRL[INP.Spe_attackA]) and ( \
        (not GMCTRL[INP.Tgl_attack_toggle]) or (
        not GMCTRL[INP.Tgl_range_toggle]
        )):
        GMCTRL[INP.Spe_attackX] = False
        GMCTRL[INP.Spe_attackY] = False
        GMCTRL[INP.Spe_attackB] = False
        GMCTRL[INP.Spe_attackA] = False

    if  GMCTRL[INP.Att_attackX] or \
        GMCTRL[INP.Att_attackY] or \
        GMCTRL[INP.Att_attackB] or \
        GMCTRL[INP.Att_attackA] or \
        GMCTRL[INP.Spe_attackX] or \
        GMCTRL[INP.Spe_attackY] or \
        GMCTRL[INP.Spe_attackB] or \
        GMCTRL[INP.Spe_attackA] or \
        GMCTRL[INP.Rng_attackX] or \
        GMCTRL[INP.Rng_attackY] or \
        GMCTRL[INP.Rng_attackB] or \
        GMCTRL[INP.Rng_attackA]:
        GMCTRL[INP.dodge] = False
        GMCTRL[INP.jump] = False
        GMCTRL[INP.roll] = False
        GMCTRL[INP.inventory] = False

    if GMCTRL[INP.nothing]:
        GMCTRL[INP.nothing] = False