"""
Progress Panel
HI Result Finder v3.1
"""

import customtkinter as ctk


class ProgressPanel(ctk.CTkFrame):

    def __init__(self, master):

        super().__init__(
            master,
            corner_radius=12
        )

        # ==========================================
        # Header
        # ==========================================

        ctk.CTkLabel(
            self,
            text="Processing Progress",
            font=("Segoe UI", 18, "bold")
        ).pack(
            anchor="w",
            padx=20,
            pady=(20, 10)
        )

        # ==========================================
        # Progress Bar
        # ==========================================

        self.progress = ctk.CTkProgressBar(
            self,
            height=18
        )

        self.progress.pack(
            fill="x",
            padx=20
        )

        self.progress.set(0)

        # ==========================================
        # Status
        # ==========================================

        self.message = ctk.CTkLabel(
            self,
            text="Waiting...",
            anchor="w"
        )

        self.message.pack(
            fill="x",
            padx=20,
            pady=(10, 15)
        )

    # ==========================================
    # Called directly by Matcher
    # ==========================================

    def update_progress(self, value, message):

        if value < 0:
            value = 0

        if value > 1:
            value = 1

        self.progress.set(value)

        self.message.configure(
            text=message
        )

    # ==========================================

    def reset(self):

        self.progress.set(0)

        self.message.configure(
            text="Waiting..."
        )