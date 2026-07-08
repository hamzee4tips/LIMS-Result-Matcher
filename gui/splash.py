"""
Professional Splash Screen
"""

import customtkinter as ctk
import os
from core.resource import resource_path
from PIL import Image


class SplashScreen(ctk.CTkToplevel):

    def __init__(self, parent):

        super().__init__(parent)

        self.overrideredirect(True)

        self.geometry("650x430")

        x = (self.winfo_screenwidth() // 2) - 325
        y = (self.winfo_screenheight() // 2) - 215

        self.geometry(f"650x430+{x}+{y}")

        frame = ctk.CTkFrame(
            self,
            corner_radius=15
        )

        frame.pack(
            fill="both",
            expand=True,
            padx=10,
            pady=10
        )

        # ======================================
        # Logo
        # ======================================

        logo_path = resource_path("assets/images/hi_result_finder.png")

        print("Logo exists:", os.path.exists(logo_path))
        print("Logo path:", logo_path)

        try:
            self.logo = ctk.CTkImage(
                light_image=Image.open(logo_path),
                dark_image=Image.open(logo_path),
                size=(140, 140)
            )
            ctk.CTkLabel(
                frame,
                image=self.logo,
                text=""
            ).pack(
                pady=(25, 10)
            )
        except Exception as e:
            print("Unable to load splash logo:", e)
            # Keep the layout identical even if the image is unavailable.
            ctk.CTkFrame(
                frame,
                width=140,
                height=140,
                fg_color="transparent"
            ).pack(
                pady=(25, 10)
            )

        # ======================================
        # Title
        # ======================================

        ctk.CTkLabel(
            frame,
            text="HI RESULT FINDER",
            font=("Segoe UI", 30, "bold")
        ).pack()

        ctk.CTkLabel(
            frame,
            text="LIMS Result Matcher",
            font=("Segoe UI", 18)
        ).pack()

        ctk.CTkLabel(
            frame,
            text="Professional Laboratory Result Matching System",
            font=("Segoe UI", 13)
        ).pack(
            pady=(8, 20)
        )

        # ======================================
        # Progress
        # ======================================

        self.progress = ctk.CTkProgressBar(
            frame,
            width=450
        )

        self.progress.pack()

        self.progress.set(0)

        self.percent = ctk.CTkLabel(
            frame,
            text="0%"
        )

        self.percent.pack(
            pady=10
        )

        ctk.CTkLabel(
            frame,
            text="Loading...",
            font=("Segoe UI", 12)
        ).pack()

        self.after(
            40,
            self.animate
        )

    def animate(self):

        value = self.progress.get()

        if value < 1:

            value += 0.02

            self.progress.set(value)

            self.percent.configure(
                text=f"{int(value*100)}%"
            )

            self.after(
                40,
                self.animate
            )
