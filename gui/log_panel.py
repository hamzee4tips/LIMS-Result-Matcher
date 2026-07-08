"""
Live Activity Log
"""

import customtkinter as ctk

from .theme import *


class LogPanel(ctk.CTkFrame):

    def __init__(self, master):

        super().__init__(master, fg_color=CARD)

        ctk.CTkLabel(
            self,
            text="Activity Log",
            font=FONT_CARD_TITLE
        ).pack(anchor="w", padx=15, pady=(10, 5))

        self.log = ctk.CTkTextbox(
            self,
            height=170
        )

        self.log.pack(fill="both", expand=True, padx=15, pady=(0, 15))

        self.write("Application started.")

    def write(self, text):

        self.log.insert("end", text + "\n")

        self.log.see("end")