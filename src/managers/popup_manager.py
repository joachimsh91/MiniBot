"""Popup message manager"""

import customtkinter as ctk

class PopupManager():
    """Popup Manager"""

    def __init__(self, root):

        self.root = root
        self.setup_popup = None

    def show_setup_popup(self, text):
        """Creates a centered setup popup."""

        # destroy old popup if it exists
        if self.setup_popup:
            self.setup_popup.destroy()

        self.setup_popup = ctk.CTkToplevel(self.root)
        self.setup_popup.title("Setup")
        self.setup_popup.resizable(False, False)

        # FORCE A GOOD WIDTH
        width = 420
        height = 140

        self.setup_popup.geometry(f"{width}x{height}")

        label = ctk.CTkLabel(
            self.setup_popup,
            text=text,
            font=("Arial", 14),
            wraplength=380  # prevents text clipping
        )
        label.pack(expand=True, fill="both", padx=20, pady=20)

        # force update for centering
        self.setup_popup.update_idletasks()

        # center on screen
        x = (self.root.winfo_screenwidth() // 2) - (width // 2)
        y = (self.root.winfo_screenheight() // 2) - (height // 2)

        self.setup_popup.geometry(f"{width}x{height}+{x}+{y}")

        # keep on top
        self.setup_popup.attributes("-topmost", True)

    def close_setup_popup(self):
        '''Closes popup window'''
        if self.setup_popup:
            self.setup_popup.destroy()
            self.setup_popup = None
