import pygame, sys, time

import json_func

print(str(time.time_ns()) + " Initialising controller.py")

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
class Game_Controls():
    moveleft = 0
    moveright = 1

    jump = 2
    roll = 3
    dodge = 4
    inventory = 5

    Tgl_attack_toggle = 6
    Tgl_range_toggle = 7

    Att_attackX = 8
    Att_attackY = 9
    Att_attackB = 10
    Att_attackA = 11

    Rng_attackX = 12
    Rng_attackY = 13
    Rng_attackB = 14
    Rng_attackA = 15

    pausegame = 16
    minimap = 17

    GUI_Left = 18
    GUI_Right = 19
    GUI_Up = 20
    GUI_Down = 21

GmCTRL = Game_Controls()
gameControls = []

settings = {}

# Initialize the joystick
pygame.joystick.init()

try:
    settings = json_func.load('main/settings.json')

    # Loads part of the settings JSON to ensure it is proper.
    settings["control_layout"]
except:
    print(f"controller_settings.json does not exist or is corrupt. Writing settings file now.")
    settings = {
        "control_layout": {}
    }

# Check for joystick
if pygame.joystick.get_count() == 0:
    print("No joystick detected")
else:
    # Use the first joystick
    joystick = pygame.joystick.Joystick(0)
    joystick.init()
    print(f"Controller {joystick.get_name()} detected!")

    isNewController = not joystick.get_name() in settings["control_layout"]
    temp = ("" if isNewController else "n\'t")
    print(f'{joystick.get_name()} has{temp} been used before.')
    if isNewController: isConfiguringController = True
    else: isConfiguringController =input(f"Do you want to change controller configuration for {joystick.get_name()}? Y = yes, not y = no? -->").lower() == "y"
    if isConfiguringController:

        settings["control_layout"][joystick.get_name()] = {}
        layout_path = settings["control_layout"][joystick.get_name()]

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
        ]

        for i in range(len(button_names)):
            listitems = lambda lst: ''.join([x + ((", " if x != lst[-2] else " and ") if x != lst[-1] else "") for x in lst])
            print(f"Controls concist of {listitems(button_names)}.")
            print(f"Bind action to {button_names[i]}:")

            previously_pushed_button = None
            confirmed_button = None
            confirmed_axis = None
            confirmed_axis_value = None
            previously_pushed_axis = None
            previously_pushed_axis_value = None

            while confirmed_button == None and confirmed_axis == None:
                for event in pygame.event.get():
                    if event.type == pygame.JOYAXISMOTION:
                        if event.value < -0.8 or event.value > 0.8 and (not (event.axis == 4 or event.axis == 5)):
                            print(f"Axis {event.axis} or {joystick_names[event.axis]} value: {event.value}")
                            if previously_pushed_axis == event.axis and previously_pushed_axis_value == round(event.value):
                                confirmed_axis = event.axis
                                confirmed_axis_value = round(event.value)
                                joystick.rumble(1, 1, 1000)
                                layout_path[button_names[i]] = {
                                    "isButton": False,
                                    "id": confirmed_axis,
                                    "axisValue": confirmed_axis_value
                                }
                                print("Wait...")
                                time.sleep(1)
                                pygame.event.get()
                                print("Confirmed!!")
                            else:
                                previously_pushed_axis = event.axis
                                previously_pushed_axis_value = round(event.value)
                                confirmed_button = None
                                print("Wait...")
                                time.sleep(1)
                                pygame.event.get()
                                print(f"Do again to confirm")
                        elif event.axis == 4 or event.axis == 5 and event.value > -0.8:
                            print(f"Triggers pressed, id={event.axis}, value={round(event.value*100)/100}")
                            if previously_pushed_axis == event.axis:
                                confirmed_axis = event.axis
                                confirmed_axis_value = 1
                                joystick.rumble(1, 1, 1000)
                                layout_path[button_names[i]] = {
                                    "isButton": False,
                                    "id": confirmed_axis,
                                    "axisValue": confirmed_axis_value
                                }
                                print("Wait...")
                                time.sleep(1)
                                pygame.event.get()
                                print("Confirmed!!")
                            else:
                                previously_pushed_axis_value = 1
                                previously_pushed_axis = event.axis
                                confirmed_button = None

                                print("Wait...")
                                time.sleep(1)
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
                                    layout_path[button_names[i]] = {
                                        "isButton": False,
                                        "id": confirmed_axis,
                                        "axisValue": confirmed_axis_value
                                    }
                                    print("Wait...")
                                    time.sleep(1)
                                    pygame.event.get()
                                    print("Confirmed!!")
                                else:
                                    confirmed_button = None
                                    previously_pushed_axis_value = round(event.value[0] if event.value[0] != 0 else event.value[1])
                                    
                                    print("Wait...")
                                    time.sleep(1)
                                    pygame.event.get()
                                    print(f"Do again to confirm")

                    elif event.type == pygame.JOYBUTTONDOWN:
                        print(f"Button {event.button} pressed")

                        if previously_pushed_button == event.button:
                            confirmed_button = event.button
                            joystick.rumble(1, 1, 1000)
                            layout_path[button_names[i]] = {
                                "isButton": True,
                                "id": confirmed_button,
                                "axisValue": None
                            }
                            print("Wait...")
                            time.sleep(1)
                            pygame.event.get()
                            print("Confirmed!")
                        else:
                            previously_pushed_button = event.button
                            confirmed_axis = None
                            confirmed_axis_value = None
                            
                            print("Wait...")
                            time.sleep(1)
                            pygame.event.get()
                            print(f"Do again to confirm")

                    elif event.type == pygame.JOYBUTTONUP:
                        print(f"Button {event.button} released")

        settings["control_layout"][joystick.get_name()] = layout_path
        print(str(time.time_ns()) + " Done!!!")
    print(str(time.time_ns()) + " Done!!")
print(str(time.time_ns()) + " Done!")
json_func.dump(settings, 'main/settings.json')

isAngleBigenough = lambda angle: angle > 0.3 or angle < -0.3
def update_input(event):
    if event.type == pygame.JOYAXISMOTION and isAngleBigenough(event.axis):
        if event.axis == 4 or event.axis == 5:
            pass
        else:
            pass
        
print(str(time.time_ns()) + " Done")