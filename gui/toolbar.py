"""
Top Toolbar
"""

import customtkinter as ctk

from .theme import *
from .about_dialog import AboutDialog


class Toolbar(ctk.CTkFrame):

    def __init__(self, master, dashboard):

        super().__init__(
            master,
            height=60,
            fg_color=CARD,
            corner_radius=10
        )

        self.dashboard = dashboard

        self.pack_propagate(False)

        buttons = [

            ("📄 Excel", self.open_excel),

            ("📕 PDF", self.open_pdf),

            ("📂 Output", self.open_output),

            ("▶ Start", self.dashboard.start_matching),

            ("⏹ Stop", self.stop_matching),

            ("🗑 Clear", self.clear_fields),

            ("ℹ About", self.show_about)

        ]

        for text, command in buttons:

            btn = ctk.CTkButton(
                self,
                text=text,
                width=110,
                height=38,
                font=FONT_BUTTON,
                command=command
            )

            btn.pack(
                side="left",
                padx=8,
                pady=10
            )

        self.status = ctk.CTkLabel(
            self,
            text="Ready",
            text_color=TEXT_SECONDARY,
            font=FONT_NORMAL
        )

        self.status.pack(
            side="right",
            padx=20
        )

    # ==========================================================
    # Status
    # ==========================================================

    def set_status(self, message):

        self.status.configure(text=message)

    # ==========================================================
    # Browse Buttons
    # ==========================================================

    def open_excel(self):

        self.dashboard.selector.browse_excel(
            self.dashboard.excel_entry
        )

    def open_pdf(self):

        self.dashboard.selector.browse_pdf(
            self.dashboard.pdf_entry
        )

    def open_output(self):

        self.dashboard.selector.browse_output(
            self.dashboard.output_entry
        )

    # ==========================================================
    # Matching Controls
    # ==========================================================

    def stop_matching(self):

        self.dashboard.matcher.stop()

        self.dashboard.log(
            "Matching stopped by user."
        )

        self.dashboard.set_status(
            "Stopped"
        )

    def clear_fields(self):

        self.dashboard.excel_entry.delete(
            0,
            "end"
        )

        self.dashboard.pdf_entry.delete(
            0,
            "end"
        )

        self.dashboard.output_entry.delete(
            0,
            "end"
        )

        self.dashboard.log(
            "Selections cleared."
        )

        self.dashboard.set_status(
            "Ready"
        )

    # ==========================================================
    # About Window
    # ==========================================================

    def show_about(self):

        AboutDialog(
            self.dashboard.root
        )