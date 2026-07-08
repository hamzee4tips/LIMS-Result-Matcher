"""
Status Bar
"""

import customtkinter as ctk
from .theme import *

class StatusBar(ctk.CTkFrame):

    def __init__(self, master):

        super().__init__(
            master,
            height=28,
            fg_color=SIDEBAR,
            corner_radius=0
        )

        self.pack_propagate(False)

        self.label = ctk.CTkLabel(
            self,
            text="Ready",
            anchor="w",
            font=FONT_SMALL,
            text_color=TEXT_SECONDARY
        )

        self.label.pack(side="left", padx=10)

        self.version = ctk.CTkLabel(
            self,
            text=f"{APP_NAME}  v{VERSION}",
            anchor="e",
            font=FONT_SMALL,
            text_color=TEXT_SECONDARY
        )

        self.version.pack(side="right", padx=10)

    def set_text(self, text):

        self.label.configure(text=text)