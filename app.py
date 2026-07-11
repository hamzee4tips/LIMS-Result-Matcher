"""
HI Result Finder
Application Entry Point
"""

import customtkinter as ctk
from core.logger import setup_logger
from tkinterdnd2 import TkinterDnD

from gui.dashboard import Dashboard
from gui.splash import SplashScreen


class App(TkinterDnD.Tk):

    def __init__(self):

        super().__init__()

        ctk.set_appearance_mode("Dark")
        ctk.set_default_color_theme("blue")

        self.withdraw()

        self.splash = SplashScreen(self)

        self.after(
            2500,
            self.start_dashboard
        )

    def start_dashboard(self):

        self.splash.destroy()

        Dashboard(self)

        self.deiconify()


if __name__ == "__main__":
    
    setup_logger()
    app = App()

    app.mainloop()