"""
Import Panel
Professional file selection workspace
"""

import customtkinter as ctk

from .drag_drop import DragDropFrame


class ImportPanel(ctk.CTkFrame):

    def __init__(self, master, dashboard):

        super().__init__(
            master,
            corner_radius=12
        )

        self.dashboard = dashboard

        # =====================================================
        # Header
        # =====================================================

        header = ctk.CTkLabel(
            self,
            text="📂  IMPORT FILES",
            font=("Segoe UI", 22, "bold")
        )

        header.pack(
            anchor="w",
            padx=20,
            pady=(20, 5)
        )

        subtitle = ctk.CTkLabel(
            self,
            text="Select the required files or simply drag and drop them below.",
            font=("Segoe UI", 13)
        )

        subtitle.pack(
            anchor="w",
            padx=20,
            pady=(0, 20)
        )

        # =====================================================
        # Excel
        # =====================================================

        self.dashboard.excel_entry = self.build_row(

            "Excel File",

            self.dashboard.selector.browse_excel

        )

        # =====================================================
        # PDF
        # =====================================================

        self.dashboard.pdf_entry = self.build_row(

            "PDF File",

            self.dashboard.selector.browse_pdf

        )

        # =====================================================
        # Output
        # =====================================================

        self.dashboard.output_entry = self.build_row(

            "Output Folder",

            self.dashboard.selector.browse_output

        )

        # =====================================================
        # Drag & Drop
        # =====================================================

        self.drag = DragDropFrame(
            self,
            dashboard
        )

        self.drag.pack(
            fill="x",
            padx=20,
            pady=(20, 15),
            ipady=20
        )

        # =====================================================
        # Buttons
        # =====================================================

        buttons = ctk.CTkFrame(
            self,
            fg_color="transparent"
        )

        buttons.pack(
            fill="x",
            padx=20,
            pady=(0, 20)
        )

        self.start_btn = ctk.CTkButton(

            buttons,

            text="▶ Start Matching",

            width=180,

            height=40,

            command=self.dashboard.start_matching

        )

        self.start_btn.pack(
            side="left"
        )

        self.clear_btn = ctk.CTkButton(

            buttons,

            text="Clear",

            width=120,

            height=40,

            fg_color="#555555",

            command=self.clear_fields

        )

        self.clear_btn.pack(
            side="left",
            padx=10
        )

    # =====================================================

    def build_row(self, title, browse_command):

        row = ctk.CTkFrame(self)

        row.pack(
            fill="x",
            padx=20,
            pady=6
        )

        label = ctk.CTkLabel(

            row,

            text=title,

            width=120,

            anchor="w"

        )

        label.pack(
            side="left",
            padx=(10, 0)
        )

        entry = ctk.CTkEntry(
            row
        )

        entry.pack(
            side="left",
            fill="x",
            expand=True,
            padx=10
        )

        browse = ctk.CTkButton(

            row,

            text="Browse",

            width=120,

            command=lambda: browse_command(entry)

        )

        browse.pack(
            side="right",
            padx=10,
            pady=10
        )

        return entry

    # =====================================================

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
            "Ready."
        )