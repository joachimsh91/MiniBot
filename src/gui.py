'''
MiniBot GUI

'''
import customtkinter as ctk
import time
import threading
import src.managers.config_manager
from datetime import datetime
from version import __version__
from src.managers.setup_manager import SetupManager
from src.managers.feature_manager import FeatureManager
from src.managers.popup_manager import PopupManager


class MiniBotGUI(ctk.CTk):
    """
    Main GUI window for MiniBot.
    Contains:
    - Feature tabs
    - Settings inputs
    - Save functionality
    - Bot controls
    """
    def __init__(self):
        """
        Initializes the GUI window and all widgets.
        """
        super().__init__()
        self.title("MiniBot")
        self.geometry("800x500")
        self.feature_manager = FeatureManager()
        self.setup_manager = SetupManager()
        self.popup_manager = PopupManager(self)
        self.last_food_time = 0
        self.last_rune_time = 0
        self.last_fish_time = 0
        self.last_tab_time = 0
        self.setup_label = None
        self.bot_running = False

        # =========================================
        # MAIN WINDOW GRID
        # =========================================

        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(0, weight=1)

        # =========================================
        # TABVIEW
        # =========================================

        self.tabs = ctk.CTkTabview(self)

        self.tabs.grid(
            row=0,
            column=0,
            sticky="nsew",
            padx=10,
            pady=10
        )

        # Create tabs
        self.tabs.add("AutoFood")
        self.tabs.add("RuneMaker")
        self.tabs.add("AutoFish")
        self.tabs.add("AutoTab")
        self.tabs.add("AutoLogout")
        self.tabs.add("About")

        # =========================================
        # CREATE TABS
        # =========================================

        self.create_food_tab()
        self.create_rune_tab()
        self.create_fish_tab()
        self.create_autotab_tab()
        self.create_logout_tab()
        self.create_about_tab()

        # =========================================
        # GLOBAL BUTTONS
        # =========================================

        self.create_global_controls()

    # ==================================================
    # TAB CREATION
    # ==================================================

    def create_food_tab(self):
        """
        Creates the AutoFood settings tab.
        """
        food_tab = self.tabs.tab("AutoFood")
        food_tab.grid_columnconfigure(0, weight=1)
        food_tab.grid_rowconfigure(0, weight=1)

        food_frame = ctk.CTkFrame(food_tab)

        food_frame.grid(
            row=0,
            column=0,
            pady=20
        )

        self.food_enabled = ctk.CTkCheckBox(
            food_frame,
            text="Enable AutoFood"
        )

        self.food_enabled.grid(
            row=0,
            column=0,
            columnspan=2,
            sticky="w",
            padx=20,
            pady=(20, 20)
        )

        # =========================================
        # FOOD HOTKEY
        # =========================================

        food_hotkey_label = ctk.CTkLabel(
            food_frame,
            text="Food Hotkey:"
        )

        food_hotkey_label.grid(
            row=1,
            column=0,
            sticky="w",
            padx=(20, 10),
            pady=10
        )

        self.food_hotkey = ctk.CTkEntry(
            food_frame,
            width=120
        )

        self.food_hotkey.grid(
            row=1,
            column=1,
            sticky="w",
            padx=(0, 20),
            pady=10
        )

        # =========================================
        # FOOD INTERVAL
        # =========================================

        food_interval_label = ctk.CTkLabel(
            food_frame,
            text="Interval (sec):"
        )

        food_interval_label.grid(
            row=2,
            column=0,
            sticky="w",
            padx=(20, 10),
            pady=10
        )

        self.food_interval = ctk.CTkEntry(
            food_frame,
            width=120
        )

        self.food_interval.grid(
            row=2,
            column=1,
            sticky="w",
            padx=(0, 20),
            pady=10
        )

        # =========================================
        # LOAD SAVED VALUES
        # =========================================

        saved_food_key = src.managers.config_manager.load_value("food_key")

        if saved_food_key:
            self.food_hotkey.insert(0, saved_food_key)

        saved_food_interval = src.managers.config_manager.load_value("food_interval")

        if saved_food_interval:
            self.food_interval.insert(
                0,
                str(saved_food_interval)
            )

        # =========================================
        # SAVE BUTTON
        # =========================================

        self.food_save = ctk.CTkButton(
            food_frame,
            text="Save Food Settings",
            command=self.save_food_settings
        )

        self.food_save.grid(
            row=3,
            column=0,
            columnspan=2,
            pady=(20, 20)
        )

    def create_rune_tab(self):
        """
        Creates the RuneMaker settings tab.
        """

        rune_tab = self.tabs.tab("RuneMaker")

        rune_tab.grid_columnconfigure(0, weight=1)
        rune_tab.grid_rowconfigure(0, weight=1)

        rune_frame = ctk.CTkFrame(rune_tab)

        rune_frame.grid(
            row=0,
            column=0,
            pady=20
        )

        self.rune_enabled = ctk.CTkCheckBox(
            rune_frame,
            text="Enable RuneMaker"
        )

        self.rune_enabled.grid(
            row=0,
            column=0,
            columnspan=2,
            sticky="w",
            padx=20,
            pady=(20, 20)
        )

        # =========================================
        # RUNE HOTKEY
        # =========================================

        rune_hotkey_label = ctk.CTkLabel(
            rune_frame,
            text="Rune Hotkey:"
        )

        rune_hotkey_label.grid(
            row=1,
            column=0,
            sticky="w",
            padx=(20, 10),
            pady=10
        )

        self.rune_hotkey = ctk.CTkEntry(
            rune_frame,
            width=120
        )

        self.rune_hotkey.grid(
            row=1,
            column=1,
            sticky="w",
            padx=(0, 20),
            pady=10
        )

        # =========================================
        # RUNE INTERVAL
        # =========================================

        rune_interval_label = ctk.CTkLabel(
            rune_frame,
            text="Interval (sec):"
        )

        rune_interval_label.grid(
            row=2,
            column=0,
            sticky="w",
            padx=(20, 10),
            pady=10
        )

        self.rune_interval = ctk.CTkEntry(
            rune_frame,
            width=120
        )

        self.rune_interval.grid(
            row=2,
            column=1,
            sticky="w",
            padx=(0, 20),
            pady=10
        )

        # =========================================
        # LOAD SAVED VALUES
        # =========================================

        saved_rune_key = src.managers.config_manager.load_value("rune_key")

        if saved_rune_key:
            self.rune_hotkey.insert(0, saved_rune_key)

        saved_rune_interval = src.managers.config_manager.load_value("rune_interval")

        if saved_rune_interval:
            self.rune_interval.insert(
                0,
                str(saved_rune_interval)
            )

        # =========================================
        # SAVE BUTTON
        # =========================================

        self.rune_save = ctk.CTkButton(
            rune_frame,
            text="Save Rune Settings",
            command=self.save_rune_settings
        )

        self.rune_save.grid(
            row=3,
            column=0,
            columnspan=2,
            pady=(20, 20)
        )

    def create_fish_tab(self):
        """
        Creates the AutoFish settings tab.
        """

        fish_tab = self.tabs.tab("AutoFish")

        fish_tab.grid_columnconfigure(0, weight=1)
        fish_tab.grid_rowconfigure(0, weight=1)

        fish_frame = ctk.CTkFrame(fish_tab)

        fish_frame.grid(
            row=0,
            column=0,
            pady=20
        )

        self.fish_enabled = ctk.CTkCheckBox(
            fish_frame,
            text="Enable AutoFish"
        )

        self.fish_enabled.grid(
            row=0,
            column=0,
            columnspan=2,
            sticky="w",
            padx=20,
            pady=(20, 20)
        )

        # =========================================
        # FISH HOTKEY
        # =========================================

        fish_hotkey_label = ctk.CTkLabel(
            fish_frame,
            text="Fishing Hotkey:"
        )

        fish_hotkey_label.grid(
            row=1,
            column=0,
            sticky="w",
            padx=(20, 10),
            pady=10
        )

        self.fish_hotkey = ctk.CTkEntry(
            fish_frame,
            width=120
        )

        self.fish_hotkey.grid(
            row=1,
            column=1,
            sticky="w",
            padx=(0, 20),
            pady=10
        )

        # =========================================
        # LOAD SAVED VALUES
        # =========================================

        saved_fish_key = src.managers.config_manager.load_value("fish_key")

        if saved_fish_key:
            self.fish_hotkey.insert(0, saved_fish_key)

        # =========================================
        # BUTTONS
        # =========================================

        self.fish_setup = ctk.CTkButton(
            fish_frame,
            text="Setup Fishing Area",
            command=self.setup_fishing_area
        )

        self.fish_setup.grid(
            row=2,
            column=0,
            columnspan=2,
            pady=(20, 10)
        )

        self.fish_save = ctk.CTkButton(
            fish_frame,
            text="Save Fishing Settings",
            command=self.save_fish_settings
        )

        self.fish_save.grid(
            row=3,
            column=0,
            columnspan=2,
            pady=(10, 20)
        )

    def create_logout_tab(self):
        """
        Creates the AutoLogout settings tab.
        """

        logout_tab = self.tabs.tab("AutoLogout")

        logout_tab.grid_columnconfigure(0, weight=1)
        logout_tab.grid_rowconfigure(0, weight=1)

        logout_frame = ctk.CTkFrame(logout_tab)

        logout_frame.grid(
            row=0,
            column=0,
            pady=20
        )

        self.logout_enabled = ctk.CTkCheckBox(
            logout_frame,
            text="Enable AutoLogout"
        )

        self.logout_enabled.grid(
            row=0,
            column=0,
            sticky="w",
            padx=20,
            pady=(20, 20)
        )

        self.logout_setup = ctk.CTkButton(
            logout_frame,
            text="Setup Battlelist",
            command=self.setup_battlelist
        )

        self.logout_setup.grid(
            row=1,
            column=0,
            padx=20,
            pady=(0, 20)
        )

    def create_about_tab(self):
        """
        Creates About tab.
        """

        about_tab = self.tabs.tab("About")

        about_tab.grid_columnconfigure(0, weight=1)
        about_tab.grid_rowconfigure(0, weight=1)

        about_frame = ctk.CTkFrame(about_tab)

        about_frame.grid(
            row=0,
            column=0,
            pady=20
        )

        title = ctk.CTkLabel(
            about_frame,
            text="MiniBot",
            font=("Arial", 28, "bold")
        )

        title.grid(
            row=0,
            column=0,
            pady=(30, 10),
            padx=40
        )

        version = ctk.CTkLabel(
            about_frame,
            text=f"Version {__version__}"
        )

        version.grid(
            row=1,
            column=0,
            pady=5
        )

        author = ctk.CTkLabel(
            about_frame,
            text="Made by j0k1m"
        )

        author.grid(
            row=2,
            column=0,
            pady=(5, 30)
        )

    def create_autotab_tab(self):
        """
        Creates the AutoTab settings tab.
        """

        autotab_tab = self.tabs.tab("AutoTab")

        # =========================================
        # TAB RESIZE CONFIGURATION
        # =========================================

        autotab_tab.grid_rowconfigure(0, weight=1)
        autotab_tab.grid_columnconfigure(0, weight=1)

        # =========================================
        # CENTER FRAME
        # =========================================

        tab_frame = ctk.CTkFrame(autotab_tab)

        tab_frame.grid(
            row=0,
            column=0,
            padx=20,
            pady=20
        )

        tab_frame.grid_columnconfigure(0, weight=0)
        tab_frame.grid_columnconfigure(1, weight=0)

        # =========================================
        # ENABLE CHECKBOX
        # =========================================

        self.tab_enabled = ctk.CTkCheckBox(
            tab_frame,
            text="Enable AutoTab"
        )

        self.tab_enabled.grid(
            row=0,
            column=0,
            columnspan=2,
            padx=20,
            pady=(10, 20),
            sticky="w"
        )

        # =========================================
        # TAB INTERVAL
        # =========================================

        tab_interval_label = ctk.CTkLabel(
            tab_frame,
            text="Interval (sec):"
        )

        tab_interval_label.grid(
            row=1,
            column=0,
            padx=(20, 10),
            pady=10,
            sticky="w"
        )

        self.tab_interval = ctk.CTkEntry(
            tab_frame,
            width=120
        )

        self.tab_interval.grid(
            row=1,
            column=1,
            padx=(0, 20),
            pady=10,
            sticky="w"
        )

        # =========================================
        # LOAD SAVED VALUE
        # =========================================

        saved_tab_interval = src.managers.config_manager.load_value("tab_interval")

        if saved_tab_interval:
            self.tab_interval.insert(
                0,
                str(saved_tab_interval)
            )

        # =========================================
        # SAVE BUTTON
        # =========================================

        self.tab_save = ctk.CTkButton(
            tab_frame,
            text="Save AutoTab Settings",
            command=self.save_autotab_settings
        )

        self.tab_save.grid(
            row=2,
            column=0,
            columnspan=2,
            pady=(20, 10)
        )

    def create_global_controls(self):
        """
        Creates global bot control buttons.
        """

        button_frame = ctk.CTkFrame(self)

        button_frame.grid(
            row=1,
            column=0,
            pady=(0, 10)
        )

        self.start_button = ctk.CTkButton(
            button_frame,
            text="Start Bot",
            command=self.start_bot
        )

        self.start_button.grid(
            row=0,
            column=0,
            padx=10,
            pady=10
        )

        self.stop_button = ctk.CTkButton(
            button_frame,
            text="Stop Bot",
            command=self.stop_bot
        )

        self.stop_button.grid(
            row=0,
            column=1,
            padx=10,
            pady=10
        )

    # ==================================================
    # SAVE FUNCTIONS
    # ==================================================

    def save_food_settings(self):
        """
        Saves AutoFood settings to config.
        """

        src.managers.config_manager.save_value(
            "food_key",
            self.food_hotkey.get()
        )

        src.managers.config_manager.save_value(
            "food_interval",
            int(self.food_interval.get())
        )

        print("[GUI] Food settings saved")

    def save_rune_settings(self):
        """
        Saves RuneMaker settings to config.
        """

        src.managers.config_manager.save_value(
            "rune_key",
            self.rune_hotkey.get()
        )

        src.managers.config_manager.save_value(
            "rune_interval",
            int(self.rune_interval.get())
        )

        print("[GUI] Rune settings saved")

    def save_fish_settings(self):
        """
        Saves AutoFish settings to config.
        """

        src.managers.config_manager.save_value(
            "fish_key",
            self.fish_hotkey.get()
        )

        print("[GUI] Fishing settings saved")

    def save_autotab_settings(self):
        """
        Saves AutoTab settings to config.
        """

        src.managers.config_manager.save_value(
            "tab_interval",
            int(self.tab_interval.get())
        )

        print("[GUI] AutoTab settings saved")

    # ==================================================
    # SETUP FUNCTIONS
    # ==================================================

    def setup_fishing_area(self):
        """Starts fishing setup in a background thread."""

        def update(step):
            # STEP 2: bottom-right instruction
            if step in ("bottom_right_prompt", "second_click"):
                self.after(0, lambda: self.popup_manager.show_setup_popup(
                    "Click BOTTOM-RIGHT corner of game window"
                ))

            # STEP 3: DONE
            elif step == "done":
                self.after(0, lambda: self.popup_manager.show_setup_popup(
                    "Fishing Setup Complete!"
                ))

                # auto close after 2 seconds
                self.after(2000, self.popup_manager.close_setup_popup)

        # STEP 0: countdown popup
        self.popup_manager.show_setup_popup("Setup starting in 5 seconds...")

        def delayed_start():
            time.sleep(5)

            # STEP 1: first instruction
            self.after(0, lambda: self.popup_manager.show_setup_popup(
                "Click TOP-LEFT corner of game window"
            ))

            # start backend AFTER delay
            self.setup_manager.setup_region("fishing_region", on_step=update)

        threading.Thread(
            target=delayed_start,
            daemon=True
        ).start()

    def setup_battlelist(self):
        """
        Starts battlelist setup.
        """

        def update(step):
            # STEP 2: bottom-right instruction
            if step in ("bottom_right_prompt", "second_click"):
                self.after(0, lambda: self.popup_manager.show_setup_popup(
                    "Click BOTTOM-RIGHT corner of battlelist"
                ))

            # STEP 3: DONE
            elif step == "done":
                self.after(0, lambda: self.popup_manager.show_setup_popup(
                    "Logout Setup Complete!"
                ))

                # auto close after 2 seconds
                self.after(2000, self.popup_manager.close_setup_popup)

                # STEP 0: countdown popup
        self.popup_manager.show_setup_popup("Setup starting in 5 seconds...")

        def delayed_start():
            time.sleep(5)

            # STEP 1: first instruction
            self.after(0, lambda: self.popup_manager.show_setup_popup(
                "Click TOP-LEFT corner of battlelist"
            ))

            # start backend AFTER delay
            self.setup_manager.setup_region("battlelist_region", on_step=update)

        threading.Thread(
            target=delayed_start,
            daemon=True
        ).start()

    # ==================================================
    # BOT CONTROL
    # ==================================================

    def bot_loop(self):
        """Bot loop"""

        print("Bot loop started")

        while self.bot_running:

            now = time.time()

            # =========================================
            # AUTO FOOD
            # =========================================

            if self.food_enabled.get():

                try:
                    key = self.food_hotkey.get().strip()
                    interval = int(self.food_interval.get())

                    if now - self.last_food_time >= interval:

                        print(
                            f"[{datetime.now().strftime('%H:%M:%S')}] "
                            f"[Food] Pressing: {key}"
                        )

                        self.feature_manager.eat_food(key)

                        self.last_food_time = now

                except Exception as e:
                    print("[Food Error]", e)

            # =========================================
            # RUNEMAKER
            # =========================================

            if self.rune_enabled.get():

                try:
                    key = self.rune_hotkey.get().strip()
                    interval = int(self.rune_interval.get())

                    if now - self.last_rune_time >= interval:

                        print(
                            f"[{datetime.now().strftime('%H:%M:%S')}] "
                            f"[Rune] Pressing: {key}"
                        )

                        self.feature_manager.make_rune(key)

                        self.last_rune_time = now

                except Exception as e:
                    print("[Rune Error]", e)

            # =========================================
            # AUTO FISH
            # =========================================

            if self.fish_enabled.get():

                try:
                    key = self.fish_hotkey.get().strip()

                    self.feature_manager.auto_fish(
                        key,
                        lambda: self.bot_running
                    )

                except Exception as e:
                    print("[Fishing Error]", e)

            # =========================================
            # AUTO TAB
            # =========================================

            if self.tab_enabled.get():

                try:
                    interval = int(self.tab_interval.get())

                    if now - self.last_tab_time >= interval:

                        print(
                            f"[{datetime.now().strftime('%H:%M:%S')}] "
                            f"[AutoTab] Pressing CTRL+TAB"
                        )

                        self.feature_manager.auto_tab()

                        self.last_tab_time = now

                except Exception as e:
                    print("[AutoTab Error]", e)

            # =========================================
            # AUTO LOGOUT
            # =========================================

            if self.logout_enabled.get():

                try:

                    danger_detected = (
                        self.feature_manager.check_safety()
                    )

                    if danger_detected:

                        print(
                            f"[{datetime.now().strftime('%H:%M:%S')}] "
                            f"[!!!] PLAYER DETECTED"
                        )

                        self.feature_manager.check_safety()

                        self.bot_running = False

                        break

                except Exception as e:
                    print("[Logout Error]", e)

            time.sleep(0.1)

    def start_bot(self):
        """
        Starts bot thread.
        """

        if self.bot_running:
            return

        print("[GUI] Bot starting in 5 seconds...")

        self.start_button.configure(state="disabled")

        self.after(5000, self.launch_bot_thread)

    def stop_bot(self):
        """Stops bot loop"""

        print("[GUI] Stopping bot...")

        self.bot_running = False

        self.start_button.configure(state="normal")

    def launch_bot_thread(self):
        """Launches bot loop thread"""

        self.bot_running = True

        threading.Thread(
            target=self.bot_loop,
            daemon=True
        ).start()
