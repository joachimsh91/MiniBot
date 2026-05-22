"""User setup manager"""

import src.managers.config_manager
from pynput import mouse

class SetupManager:
    """Manages all user setup"""

    def __init__(self, region=None):

        self.region = region

    def setup_region(self, key, on_step=None):
        """
        One-time setup for selecting the area.
        Saves coordinates automatically to setup.json
        """

        coords = []

        print("Setup starts in 5 seconds...")

        if on_step:
            on_step("top_left")

        def on_click(x, y, button, pressed):
            if pressed and button == mouse.Button.left:
                coords.append((int(x), int(y)))

                if len(coords) == 1:
                    if on_step:
                        on_step("bottom_right_prompt")

                elif len(coords) == 2:
                    return False  # stop listener

        with mouse.Listener(on_click=on_click) as listener:
            listener.join()

        x1, y1 = coords[0]
        x2, y2 = coords[1]

        left = min(x1, x2)
        top = min(y1, y2)

        width = abs(x1 - x2)
        height = abs(y1 - y2)

        self.region = (left, top, width, height)

        src.managers.config_manager.save_region(self.region, key)

        if on_step:
            on_step("done")

        print(f"[Setup] Done! Region set to: {self.region}")
