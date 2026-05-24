'''
MiniBot features

'''

import pyautogui
from src.auto_fishing import FishingBot
from src.auto_logout import Autologger

class FeatureManager:
    '''Mangages all features'''
    def __init__(self):
        self.fishing_bot = FishingBot()
        self.logout_bot = Autologger()
        self.last_food_time = 0
        self.last_rune_time = 0

    def get_food_setup(self):
        "Assign hotkey to AutoFood function"
        return input("Please type in the hotkey assigned to your food: ")

    def get_rune_setup(self):
        "Assign hotkey to RuneMaker function"
        return input("Please type in the hotkey assigned to the rune: ")

    def get_fishing_setup(self):
        "Assign hotkey to AutoFish function"
        return input("Please type in the hotkey assigned to the fishing rod: ")

    def get_food_interval(self):
        "Set time interval for eating food"
        return int(input("Please type in the time interval for eating food: "))

    def get_rune_interval(self):
        "Set time interval for making rune"
        return int(input("Please type in the time interval for making rune: "))

    def get_tab_interval(self):
        "Set time interval for switching tab"
        return int(input("Please type in the time interval for switching tab: "))

    def eat_food(self, key):
        '''AutoEat feature'''
        pyautogui.press(key)

    def make_rune(self, key):
        """Presses rune hotkey"""
        key = str(key).strip().lower()
        pyautogui.press(key)

    def auto_tab(self):
        """Changes browser tab"""
        pyautogui.hotkey("ctrl", "tab")

    def auto_fish(self, key, should_continue):
        '''AutoFish feature'''
        self.fishing_bot.run_cycle(
        key,
        should_continue
        )

    def check_safety(self):
        """This should be called in every loop of the main script."""
        if self.logout_bot.scan_for_danger():
            self.logout_bot.logout()
            return True # Returns True so main loop can stop
        return False
