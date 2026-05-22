"""
Fishing module
"""

import cv2
import numpy as np
import pyautogui
import time
import random
import src.managers.config_manager
from datetime import datetime

class FishingBot:
    '''AutoFish'''
    def __init__(self, region=None):
        # If region is None, the user must run setup_region()
        self.region = region or src.managers.config_manager.load_region("fishing_region")
        self.tile_size = 32
        self.max_tiles = 12
        self.lower_blue = np.array([90, 50, 50])
        self.upper_blue = np.array([130, 255, 255])

        # State/Memory
        self.cached_tiles = []
        self.last_execution = 0
        self.next_interval = 20

    def _get_unique_water_tiles(self):
        if not self.region:
            print("[Error] Region not defined. Run setup_region() first.")
            return []

        screenshot = pyautogui.screenshot(region=self.region)
        img = cv2.cvtColor(np.array(screenshot), cv2.COLOR_RGB2BGR)
        hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
        mask = cv2.inRange(hsv, self.lower_blue, self.upper_blue)

        unique_tiles = []
        reg_x, reg_y, reg_w, reg_h = self.region

        for y in range(self.tile_size, reg_h - self.tile_size, self.tile_size):
            for x in range(self.tile_size, reg_w - self.tile_size, self.tile_size):
                checks = [
                    mask[y:y+self.tile_size, x:x+self.tile_size],
                    mask[y-self.tile_size:y, x:x+self.tile_size],
                    mask[y+self.tile_size:y+(self.tile_size*2), x:x+self.tile_size],
                    mask[y:y+self.tile_size, x-self.tile_size:x],
                    mask[y:y+self.tile_size, x+self.tile_size:x+(self.tile_size*2)]
                ]

                water_threshold = self.tile_size**2 * 0.95
                is_safe = all(a.size > 0 and cv2.countNonZero(a) > water_threshold for a in checks)

                if is_safe:
                    unique_tiles.append((x + reg_x + 16, y + reg_y + 16))
                    if len(unique_tiles) >= self.max_tiles:
                        break

        return unique_tiles

    def run_cycle(self, hotkey, should_continue):
        '''Runs a fishing cycle'''

        current_time = time.time()
        if (current_time - self.last_execution) < self.next_interval:
            return

        if not self.cached_tiles:
            print("[Fishing] Scanning for water...")
            self.cached_tiles = self._get_unique_water_tiles()
            if not self.cached_tiles:
                print("[Fishing] No water tiles found, retrying in 10s...")
                self.last_execution = current_time + 10
                return
        print(
              f"[{datetime.now().strftime('%H:%M:%S')}] "
              f"[Fishing] Round started with key: {hotkey}"
             )


        random.shuffle(self.cached_tiles)

        for tile in self.cached_tiles:

            if not should_continue():

                print("[Fishing] Cycle interrupted")

                return

            pyautogui.press(hotkey)

            time.sleep(random.uniform(0.2, 0.4))

            pyautogui.click(tile)

            time.sleep(random.uniform(1.6, 2.2))

        self.last_execution = time.time()
        self.next_interval = random.uniform(15, 35)
