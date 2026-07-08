"""
About Dialog
"""

import customtkinter as ctk
import webbrowser

from version import (
    APP_NAME,
    APP_BRAND,
    VERSION,
    BUILD,
    RELEASE_DATE,
    DEVELOPER,
    COMPANY,
    COPYRIGHT,
    DESCRIPTION,
    GITHUB,
)


class AboutDialog(ctk.CTkToplevel):

    def __init__(self, parent):

        super().__init__(parent)

        self.title(f"About {APP_BRAND}")

        self.geometry("550x520")

        self.resizable(False, False)

        self.grab_set()

        self.transient(parent)

        # ==============================
        # Header
        # ==============================

        ctk.CTkLabel(
            self,
            text=APP_BRAND,
            font=("Segoe UI", 28, "bold")
        ).pack(pady=(25, 5))

        ctk.CTkLabel(
            self,
            text=APP_NAME,
            font=("Segoe UI", 18)
        ).pack()

        ctk.CTkLabel(
            self,
            text=DESCRIPTION,
            font=("Segoe UI", 13)
        ).pack(pady=(5, 20))

        # ==============================
        # Information Panel
        # ==============================

        info = ctk.CTkFrame(self)

        info.pack(
            fill="x",
            padx=30,
            pady=10
        )

        rows = [

            ("Version", VERSION),

            ("Build", BUILD),

            ("Release Date", RELEASE_DATE),

            ("Developer", DEVELOPER),

            ("Company", COMPANY)

        ]

        for title, value in rows:

            row = ctk.CTkFrame(
                info,
                fg_color="transparent"
            )

            row.pack(
                fill="x",
                padx=15,
                pady=6
            )

            ctk.CTkLabel(
                row,
                text=f"{title}:",
                width=120,
                anchor="w",
                font=("Segoe UI", 13, "bold")
            ).pack(side="left")

            ctk.CTkLabel(
                row,
                text=value,
                anchor="w"
            ).pack(side="left")

        # ==============================
        # GitHub
        # ==============================

        ctk.CTkButton(
            self,
            text="🌐 Visit GitHub Repository",
            width=250,
            command=lambda: webbrowser.open(GITHUB)
        ).pack(pady=(25, 10))

        # ==============================
        # Copyright
        # ==============================

        ctk.CTkLabel(
            self,
            text=COPYRIGHT,
            justify="center"
        ).pack(pady=(10, 5))

        # ==============================
        # Close Button
        # ==============================

        ctk.CTkButton(
            self,
            text="Close",
            width=140,
            command=self.destroy
        ).pack(pady=(20, 25))