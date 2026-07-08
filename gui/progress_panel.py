"""
Progress Panel
"""

import customtkinter as ctk
from .theme import *


class ProgressPanel(ctk.CTkFrame):

    def __init__(self, master):

        super().__init__(master, fg_color=CARD)

        ctk.CTkLabel(
            self,
            text="Processing Progress",
            font=FONT_CARD_TITLE
        ).pack(anchor="w", padx=15, pady=(10, 5))

        self.progress = ctk.CTkProgressBar(self)

        self.progress.pack(fill="x", padx=15, pady=5)

        self.progress.set(0)

        self.info = ctk.CTkLabel(
            self,
            text="Waiting to start...",
            text_color=TEXT_SECONDARY
        )

        self.info.pack(anchor="w", padx=15, pady=(0, 10))

    def update_progress(self, value, message):

        self.progress.set(value)

        self.info.configure(text=message)