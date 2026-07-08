"""
Professional Drag & Drop Widget v2.0
Requires:
    pip install tkinterdnd2
"""

import os
import customtkinter as ctk

try:
    from tkinterdnd2 import DND_FILES

    DND_AVAILABLE = True

except ImportError:

    DND_AVAILABLE = False


class DragDropFrame(ctk.CTkFrame):

    def __init__(self, master, dashboard):

        super().__init__(
            master,
            corner_radius=12,
            border_width=2
        )

        self.dashboard = dashboard

        self.normal_border = "gray60"
        self.hover_border = "#2F80ED"
        self.success_border = "#27AE60"

        self.processing = False

        self.configure(border_color=self.normal_border)

        self.label = ctk.CTkLabel(
            self,
            text=(
                "📂\n\n"
                "Drop Excel or PDF Files Here\n\n"
                "or click Browse above\n\n"
                "Supported Files\n"
                "✓ Excel (.xlsx, .xls)\n"
                "✓ PDF (.pdf)"
            ),
            justify="center",
            font=("Segoe UI", 16)
        )

        self.label.pack(
            expand=True,
            fill="both",
            padx=20,
            pady=25
        )

        # Double-click to browse
        self.label.bind(
            "<Double-Button-1>",
            self.double_click
        )

        self.bind(
            "<Double-Button-1>",
            self.double_click
        )

        if DND_AVAILABLE:

            self.drop_target_register(DND_FILES)

            self.dnd_bind(
                "<<DropEnter>>",
                self.on_enter
            )

            self.dnd_bind(
                "<<DropLeave>>",
                self.on_leave
            )

            self.dnd_bind(
                "<<Drop>>",
                self.on_drop
            )

    # ----------------------------------------------------

    def double_click(self, event):

        self.dashboard.selector.browse_excel(
            self.dashboard.excel_entry
        )

    # ----------------------------------------------------

    def on_enter(self, event):

        if not self.processing:

            self.configure(
                border_color=self.hover_border
            )

        return event.action

    # ----------------------------------------------------

    def on_leave(self, event):

        if not self.processing:

            self.configure(
                border_color=self.normal_border
            )

        return event.action

    # ----------------------------------------------------

    def on_drop(self, event):

        if self.processing:

            return event.action

        self.processing = True

        self.after(
            80,
            lambda: self.process_drop(event.data)
        )

        return event.action

    # ----------------------------------------------------

    def process_drop(self, raw):

        try:

            files = self.tk.splitlist(raw)

            excel_files = []

            pdf_files = []

            for item in files:

                path = item.strip("{}")

                if os.path.isdir(path):

                    self.dashboard.log(
                        "Folder dropped."
                    )

                    self.dashboard.set_status(
                        "Folders are not supported."
                    )

                    self.finish(False)

                    return

                lower = path.lower()

                if lower.endswith((".xlsx", ".xls")):

                    excel_files.append(path)

                elif lower.endswith(".pdf"):

                    pdf_files.append(path)

                else:

                    self.dashboard.log(
                        f"Unsupported file:\n{path}"
                    )

                    self.dashboard.set_status(
                        "Unsupported file."
                    )

                    self.finish(False)

                    return

            if len(excel_files) > 1:

                self.dashboard.log(
                    "Multiple Excel files detected."
                )

                self.dashboard.set_status(
                    "Drop only one Excel file."
                )

                self.finish(False)

                return

            if len(pdf_files) > 1:

                self.dashboard.log(
                    "Multiple PDF files detected."
                )

                self.dashboard.set_status(
                    "Drop only one PDF file."
                )

                self.finish(False)

                return

            if excel_files:

                self.dashboard.excel_entry.delete(
                    0,
                    "end"
                )

                self.dashboard.excel_entry.insert(
                    0,
                    excel_files[0]
                )

                self.dashboard.log(
                    f"Excel loaded:\n{excel_files[0]}"
                )

            if pdf_files:

                self.dashboard.pdf_entry.delete(
                    0,
                    "end"
                )

                self.dashboard.pdf_entry.insert(
                    0,
                    pdf_files[0]
                )

                self.dashboard.log(
                    f"PDF loaded:\n{pdf_files[0]}"
                )

            if excel_files and pdf_files:

                self.dashboard.set_status(
                    "Excel and PDF loaded."
                )

            elif excel_files:

                self.dashboard.set_status(
                    "Excel loaded."
                )

            elif pdf_files:

                self.dashboard.set_status(
                    "PDF loaded."
                )

            self.finish(True)

        except Exception as e:

            self.dashboard.log(
                f"Drag & Drop Error: {e}"
            )

            self.dashboard.set_status(
                "Drag & Drop failed."
            )

            self.finish(False)

    # ----------------------------------------------------

    def finish(self, success):

        if success:

            self.configure(
                border_color=self.success_border
            )

        else:

            self.configure(
                border_color=self.normal_border
            )

        self.after(
            1500,
            self.reset
        )

    # ----------------------------------------------------

    def reset(self):

        self.processing = False

        self.configure(
            border_color=self.normal_border
        )