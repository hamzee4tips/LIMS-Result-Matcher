"""
Sidebar Navigation
"""

import customtkinter as ctk
from .theme import *

class Sidebar(ctk.CTkFrame):

    def __init__(self, master):

        super().__init__(
            master,
            width=220,
            fg_color=SIDEBAR,
            corner_radius=0
        )

        self.pack_propagate(False)

        ctk.CTkLabel(
            self,
            text="HI\nResult Finder",
            font=("Segoe UI", 22, "bold"),
            text_color="white"
        ).pack(pady=(30, 40))

        self.create_button("🏠 Dashboard")
        self.create_button("📂 Match Results")
        self.create_button("🔍 Search PepID")
        self.create_button("📊 Reports")
        self.create_button("📜 Activity Log")
        self.create_button("⚙ Settings")

        ctk.CTkLabel(
            self,
            text="────────────",
            text_color="gray"
        ).pack(pady=20)

        self.create_button("❓ Help")
        self.create_button("ℹ About")

        ctk.CTkLabel(
            self,
            text=f"Version {VERSION}",
            text_color="gray"
        ).pack(side="bottom", pady=20)

    def create_button(self, text):

        button = ctk.CTkButton(
            self,
            text=text,
            anchor="w",
            height=42,
            corner_radius=8,
            font=FONT_BUTTON
        )

        button.pack(fill="x", padx=15, pady=5)