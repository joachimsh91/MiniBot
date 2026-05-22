"""
Autologger module

"""

import cv2
import numpy as np
import pyautogui
import time
import src.managers.config_manager

class Autologger:
    '''Autologout when health bar appears in battlelist'''
    def __init__(self, region=None):
        # Load saved battlelist region from setup.json
        self.region = region or src.managers.config_manager.load_region("battlelist_region")

        # HSV values for green health bars
        self.lower_green = np.array([40, 100, 100])
        self.upper_green = np.array([70, 255, 255])

    def scan_for_danger(self):
        """
        Returns True if a green health bar is detected
        in the battle list.
        """

        screenshot = pyautogui.screenshot(region=self.region)

        img = cv2.cvtColor(np.array(screenshot), cv2.COLOR_RGB2BGR)

        hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)

        # Create mask for green colors
        mask = cv2.inRange(hsv, self.lower_green, self.upper_green)

        # Count green pixels
        green_pixels = cv2.countNonZero(mask)

        # Ignore tiny noise
        if green_pixels > 15:
            print(f"[Autologger] Danger detected ({green_pixels} green pixels)")
            return True

        return False

    def logout(self):
        """Logout when player is detected"""
        print("[!!!] PLAYER DETECTED - LOGGING OUT IMMEDIATELY")

        pyautogui.hotkey('ctrl', 'l')

        time.sleep(0.2)

        pyautogui.press('enter')

        time.sleep(0.2)

        pyautogui.press('enter')
