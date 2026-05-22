'''
MiniBot Entry Point
'''

import customtkinter as ctk
from src.gui import MiniBotGUI

if __name__ == "__main__":

    ctk.set_appearance_mode("dark")

    app = MiniBotGUI()

    app.mainloop()
