import input_ID as INP


class Layout:
    def __init__(self):
        """
        This is a class that stores the information about all of the title screens.
        
        ***
        ### Menu screens

        This is what menu screen shows at the beginning of the game.
        ```
        layout.startup
        ```

        This is what menu screen shows when the game is paused.
        ```
        layout.pausegame
        ```

        This is what menu screen shows when you're ingame.
        ```
        layout.ingame
        ```

        ***
        ### Actual layout

        The layout is storerd in
        ```
        layout.layout
        ```
        I know, right? *So* complicated and obsure. Anyways, `layout.layout` is stored in a dictionary. If you want to learn how it works, then read the 232 lines of code right down below!
        """
        self.startup = "main_menu"

        # This is what menu screen happens when the pause button is pressed while playing
        self.pausegame = "ingame/pausemenu"

        # This is what menu screen happens when ingame
        self.ingame = "ingame"

        self.layout = {
            "main_menu": {
                "max_buttons": 3,
                "starting_point": (2, -1),
                "buttons": [
                    {
                        "image": "game.GUI.assets.title_logo",
                        "image_hover": None,
                        "image_push": None,
                        "anim": 0,
                        "anim_positive": True,
                        "pos_multiplier": (0, -2),
                        "button_assignment": None,
                        "text": None,
                        "button_push": None,
                        "button_push_menu_screen": "main_menu"
                    },
                    {
                        "image": "game.GUI.assets.menu_buttons[0]",
                        "image_hover": "game.GUI.assets.menu_buttons_selected[0]",
                        "image_push": "game.GUI.assets.menu_buttons_push[0]",
                        "anim": 1,
                        "anim_positive": False,
                        "pos_multiplier": (0, 0),
                        "button_assignment": 0,
                        "text": ("Start Game", True, (255, 255, 255)),
                        "button_push": INP.GUI_A,
                        "button_push_menu_screen": "main_menu/choose_gamemode"
                    },
                    {
                        "image": "game.GUI.assets.menu_buttons[1]",
                        "image_hover": "game.GUI.assets.menu_buttons_selected[1]",
                        "image_push": "game.GUI.assets.menu_buttons_push[1]",
                        "anim": 2,
                        "anim_positive": True,
                        "pos_multiplier": (0, 1),
                        "button_assignment": 1,
                        "text": ("Exit", True, (255, 255, 255)),
                        "button_push": INP.GUI_B,
                        "button_push_menu_screen": "main_menu"
                    },
                    {
                        "image": "game.GUI.assets.menu_buttons[2]",
                        "image_hover": "game.GUI.assets.menu_buttons_selected[2]",
                        "image_push": "game.GUI.assets.menu_buttons_push[2]",
                        "anim": 1,
                        "anim_positive": False,
                        "pos_multiplier": (1, 0),
                        "button_assignment": 2,
                        "text": ("Settings", True, (255, 255, 255)),
                        "button_push": INP.GUI_X,
                        "button_push_menu_screen": "main_menu"
                    },
                    {
                        "image": "game.GUI.assets.menu_buttons[3]",
                        "image_hover": "game.GUI.assets.menu_buttons_selected[3]",
                        "image_push": "game.GUI.assets.menu_buttons_push[3]",
                        "anim": 2,
                        "anim_positive": True,
                        "pos_multiplier": (1, 1),
                        "button_assignment": 3,
                        "text": ("Credits", True, (255, 255, 255)),
                        "button_push": INP.GUI_Y,
                        "button_push_menu_screen": "main_menu/credits"
                    },
                ]
            },
            "main_menu/credits": {
                "max_buttons": 0,
                "starting_point": (2, 1),
                "buttons": [
                    {
                        "image": None,
                        "image_hover": None,
                        "image_push": None,
                        "anim": 1,
                        "anim_positive": False,
                        "pos_multiplier": (0, 0),
                        "button_assignment": None,
                        "text": ("This Game...", True, (255, 255, 255)),
                        "button_push": None,
                        "button_push_menu_screen": "main_menu"
                    },
                    {
                        "image": None,
                        "image_hover": None,
                        "image_push": None,
                        "anim": 1,
                        "anim_positive": False,
                        "pos_multiplier": (1, 0),
                        "button_assignment": None,
                        "text": ("Is Made By...", True, (255, 255, 255)),
                        "button_push": None,
                        "button_push_menu_screen": "main_menu"
                    },
                    {
                        "image": None,
                        "image_hover": None,
                        "image_push": None,
                        "anim": 1,
                        "anim_positive": False,
                        "pos_multiplier": (0, 1),
                        "button_assignment": None,
                        "text": ("Game made by 60Trees_", True, (3, 150, 5)),
                        "button_push": None,
                        "button_push_menu_screen": "main_menu"
                    },
                    {
                        "image": None,
                        "image_hover": None,
                        "image_push": None,
                        "anim": 1,
                        "anim_positive": False,
                        "pos_multiplier": (1, 1),
                        "button_assignment": None,
                        "text": ("Some assets made by Alex <3", True, (3, 150, 5)),
                        "button_push": None,
                        "button_push_menu_screen": "main_menu"
                    },
                    {
                        "image": "game.GUI.assets.menu_buttons[1]",
                        "image_hover": "game.GUI.assets.menu_buttons_selected[1]",
                        "image_push": "game.GUI.assets.menu_buttons_push[1]",
                        "anim": 2,
                        "anim_positive": True,
                        "pos_multiplier": (0.5, 2),
                        "button_assignment": 0,
                        "text": ("Back", True, (255, 255, 255)),
                        "button_push": INP.GUI_B,
                        "button_push_menu_screen": "main_menu"
                    },
                ]
            },
            "main_menu/choose_gamemode": {
                "max_buttons": 2,
                "starting_point": (2, 1),
                "buttons": [
                    {
                        "image": "game.GUI.assets.menu_buttons[4]",
                        "image_hover": "game.GUI.assets.menu_buttons_selected[4]",
                        "image_push": "game.GUI.assets.menu_buttons_push[4]",
                        "anim": 1,
                        "anim_positive": False,
                        "pos_multiplier": (0, 0),
                        "button_assignment": 0,
                        "text": ("Start Game", True, (255, 255, 255)),
                        "button_push": None,
                        "button_push_menu_screen": "ingame"
                    },
                    {
                        "image": "game.GUI.assets.menu_buttons[1]",
                        "image_hover": "game.GUI.assets.menu_buttons_selected[1]",
                        "image_push": "game.GUI.assets.menu_buttons_push[1]",
                        "anim": 2,
                        "anim_positive": True,
                        "pos_multiplier": (0.5, 2),
                        "button_assignment": 1,
                        "text": ("Back", True, (255, 255, 255)),
                        "button_push": INP.GUI_B,
                        "button_push_menu_screen": "main_menu"
                    },
                    {
                        "image": "game.GUI.assets.menu_buttons[2]",
                        "image_hover": "game.GUI.assets.menu_buttons_selected[2]",
                        "image_push": "game.GUI.assets.menu_buttons_push[2]",
                        "anim": 1,
                        "anim_positive": False,
                        "pos_multiplier": (1, 0),
                        "button_assignment": 2,
                        "text": ("Tuotorial", True, (150, 150, 150)),
                        "button_push": INP.GUI_X,
                        "button_push_menu_screen": "main_menu"
                    },
                ]
            },
            "ingame/pausemenu": {
                "max_buttons": 3,
                "starting_point": (2, -1),
                "buttons": [
                    {
                        "image": "game.GUI.assets.title_logo",
                        "image_hover": None,
                        "image_push": None,
                        "anim": 0,
                        "anim_positive": True,
                        "pos_multiplier": (0, -2),
                        "button_assignment": None,
                        "text": None,
                        "button_push": None,
                        "button_push_menu_screen": "main_menu"
                    },
                    {
                        "image": "game.GUI.assets.menu_buttons[0]",
                        "image_hover": "game.GUI.assets.menu_buttons_selected[0]",
                        "image_push": "game.GUI.assets.menu_buttons_push[0]",
                        "anim": 1,
                        "anim_positive": False,
                        "pos_multiplier": (0, 0),
                        "button_assignment": 0,
                        "text": ("Resume Game", True, (255, 255, 255)),
                        "button_push": INP.GUI_A,
                        "button_push_menu_screen": "ingame"
                    },
                    {
                        "image": "game.GUI.assets.menu_buttons[1]",
                        "image_hover": "game.GUI.assets.menu_buttons_selected[1]",
                        "image_push": "game.GUI.assets.menu_buttons_push[1]",
                        "anim": 2,
                        "anim_positive": True,
                        "pos_multiplier": (0, 1),
                        "button_assignment": 1,
                        "text": ("Quit to Title", True, (255, 255, 255)),
                        "button_push": INP.GUI_B,
                        "button_push_menu_screen": "main_menu"
                    },
                    {
                        "image": "game.GUI.assets.menu_buttons[2]",
                        "image_hover": "game.GUI.assets.menu_buttons_selected[2]",
                        "image_push": "game.GUI.assets.menu_buttons_push[2]",
                        "anim": 1,
                        "anim_positive": False,
                        "pos_multiplier": (1, 0),
                        "button_assignment": 2,
                        "text": ("Options", True, (255, 255, 255)),
                        "button_push": INP.GUI_X,
                        "button_push_menu_screen": "ingame/pausemenu/options"
                    },
                    {
                        "image": "game.GUI.assets.menu_buttons[3]",
                        "image_hover": "game.GUI.assets.menu_buttons_selected[3]",
                        "image_push": "game.GUI.assets.menu_buttons_push[3]",
                        "anim": 2,
                        "anim_positive": True,
                        "pos_multiplier": (1, 1),
                        "button_assignment": 3,
                        "text": ("Accesibility settings", True, (255, 255, 255)),
                        "button_push": INP.GUI_Y,
                        "button_push_menu_screen": "ingame"
                    },
                ]
            },
            "ingame/pausemenu/options": {
                "max_buttons": 2,
                "starting_point": (0, 0),
                "buttons": [
                    {
                        "image": "game.GUI.assets.menu_buttons[0]",
                        "image_hover": "game.GUI.assets.menu_buttons_selected[0]",
                        "image_push": "game.GUI.assets.menu_buttons_push[0]",
                        "anim": 1,
                        "anim_positive": False,
                        "pos_multiplier": (0, 1),
                        "button_assignment": 1,
                        "text": ("Resume Game", True, (255, 255, 255)),
                        "button_push": INP.GUI_A,
                        "button_push_menu_screen": "ingame"
                    },
                    {
                        "image": "game.GUI.assets.menu_buttons[1]",
                        "image_hover": "game.GUI.assets.menu_buttons_selected[1]",
                        "image_push": "game.GUI.assets.menu_buttons_push[1]",
                        "anim": 2,
                        "anim_positive": True,
                        "pos_multiplier": (1, 1),
                        "button_assignment": 2,
                        "text": ("Quit to Title", True, (255, 255, 255)),
                        "button_push": INP.GUI_B,
                        "button_push_menu_screen": "main_menu"
                    },
                    {
                        "image": "game.GUI.assets.menu_buttons[2]",
                        "image_hover": "game.GUI.assets.menu_buttons_selected[2]",
                        "image_push": "game.GUI.assets.menu_buttons_push[2]",
                        "anim": 1,
                        "anim_positive": False,
                        "pos_multiplier": (0, 0),
                        "button_assignment": 0,
                        "text": ("You are in options", True, (255, 255, 255)),
                        "button_push": INP.GUI_X,
                        "button_push_menu_screen": "ingame"
                    },
                ]
            },
        }

        # That's the layout i guess
    def is_paused(self, current_menu):
        return self.pausegame in current_menu and current_menu != self.ingame