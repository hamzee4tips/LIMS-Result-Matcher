"""
Main Dashboard
"""

import customtkinter as ctk

from .theme import *

from .sidebar import Sidebar
from .toolbar import Toolbar
from .statusbar import StatusBar
from .progress_panel import ProgressPanel
from .log_panel import LogPanel
from .completion_dialog import CompletionDialog
from .import_panel import ImportPanel

from core.settings import SettingsManager
from core.matcher import Matcher
from .file_selector import FileSelector


class Dashboard:

    def __init__(self, root):

        self.root = root

        self.settings = SettingsManager.load()

        self.selector = FileSelector()

        self.matcher = Matcher(self)

        # --------------------------------------------------

        self.root.title(APP_NAME)

        self.root.geometry(f"{WINDOW_WIDTH}x{WINDOW_HEIGHT}")

        self.root.minsize(1250, 760)

        # --------------------------------------------------
        # Sidebar
        # --------------------------------------------------

        self.sidebar = Sidebar(self.root)

        self.sidebar.pack(
            side="left",
            fill="y"
        )

        # --------------------------------------------------
        # Main Container
        # --------------------------------------------------

        self.main = ctk.CTkFrame(
            self.root,
            fg_color=BACKGROUND
        )

        self.main.pack(
            side="left",
            fill="both",
            expand=True
        )

        # --------------------------------------------------
        # Toolbar
        # --------------------------------------------------

        self.toolbar = Toolbar(
            self.main,
            self
        )

        self.toolbar.pack(
            fill="x",
            padx=15,
            pady=(15, 10)
        )

        # --------------------------------------------------
        # Workspace
        # --------------------------------------------------

        self.workspace = ctk.CTkFrame(
            self.main,
            fg_color="transparent"
        )

        self.workspace.pack(
            fill="both",
            expand=True,
            padx=15,
            pady=(0, 10)
        )

        # ==================================================
        # LEFT SIDE
        # ==================================================

        self.left_panel = ctk.CTkFrame(
            self.workspace,
            corner_radius=12
        )

        self.left_panel.pack(
            side="left",
            fill="both",
            expand=True,
            padx=(0, 10)
        )

        # ==================================================
        # RIGHT SIDE
        # ==================================================

        self.right_panel = ctk.CTkFrame(
            self.workspace,
            width=340,
            corner_radius=12
        )

        self.right_panel.pack(
            side="right",
            fill="y"
        )

        self.right_panel.pack_propagate(False)

        # ==================================================
        # Import Panel
        # ==================================================

        self.import_panel = ImportPanel(
            self.left_panel,
            self
        )

        self.import_panel.pack(
            fill="x",
            padx=15,
            pady=15
        )

        # ==================================================
        # Activity Log
        # ==================================================

        self.log_panel = LogPanel(
            self.left_panel
        )

        self.log_panel.pack(
            fill="both",
            expand=True,
            padx=15,
            pady=(0, 15)
        )

        self.log(
            "Dashboard loaded successfully."
        )

        self.log(
            "Ready."
        )

        # ==================================================
        # Progress
        # ==================================================

        self.progress_panel = ProgressPanel(
            self.right_panel
        )

        self.progress_panel.pack(
            fill="x",
            padx=15,
            pady=(15, 10)
        )

        self.progress_panel.update_progress(
            0,
            "Waiting..."
        )

        # ==================================================
        # Statistics
        # ==================================================

        stats = ctk.CTkFrame(
            self.right_panel
        )

        stats.pack(
            fill="x",
            padx=15,
            pady=10
        )

        self.found_card = self.card(
            stats,
            "Found",
            "0"
        )

        self.missing_card = self.card(
            stats,
            "Missing",
            "0"
        )

        self.duplicate_card = self.card(
            stats,
            "Duplicate",
            "0"
        )

        self.unreadable_card = self.card(
            stats,
            "Unreadable",
            "0"
        )

        # ==================================================
        # Status
        # ==================================================

        self.status = StatusBar(
            self.main
        )

        self.status.pack(
            side="bottom",
            fill="x"
        )
    # ==========================================================
    # Statistics Card
    # ==========================================================

    def card(self, parent, title, value):

        frame = ctk.CTkFrame(
            parent,
            width=145,
            height=85,
            corner_radius=10
        )

        frame.pack(
            fill="x",
            padx=8,
            pady=6
        )

        frame.pack_propagate(False)

        ctk.CTkLabel(
            frame,
            text=title,
            font=FONT_CARD_TITLE
        ).pack(
            pady=(10, 0)
        )

        value_label = ctk.CTkLabel(
            frame,
            text=value,
            font=FONT_CARD_VALUE
        )

        value_label.pack(expand=True)

        return value_label

    # ==========================================================
    # Logging
    # ==========================================================

    def log(self, message):

        if hasattr(self, "log_panel"):

            self.log_panel.write(message)

    # ==========================================================
    # Status
    # ==========================================================

    def set_status(self, message):

        if hasattr(self, "status"):

            self.status.set_text(message)

        if hasattr(self, "toolbar"):

            try:

                self.toolbar.set_status(message)

            except Exception:

                pass

    # ==========================================================
    # Statistics
    # ==========================================================

    def update_statistics(

        self,

        found,

        missing,

        duplicate,

        unreadable

    ):

        self.root.after(

            0,

            lambda: self.found_card.configure(

                text=str(found)

            )

        )

        self.root.after(

            0,

            lambda: self.missing_card.configure(

                text=str(missing)

            )

        )

        self.root.after(

            0,

            lambda: self.duplicate_card.configure(

                text=str(duplicate)

            )

        )

        self.root.after(

            0,

            lambda: self.unreadable_card.configure(

                text=str(unreadable)

            )

        )

    # ==========================================================
    # Progress
    # ==========================================================

    def update_progress(

        self,

        percent,

        message=""

    ):

        if hasattr(

            self,

            "progress_panel"

        ):

            self.progress_panel.update_progress(

                percent,

                message

            )
    # ==========================================================
    # Start Matching
    # ==========================================================

    def start_matching(self):

        excel = self.excel_entry.get().strip()
        pdf = self.pdf_entry.get().strip()
        output = self.output_entry.get().strip()

        if not excel:

            self.log("Please select an Excel file.")
            self.set_status("Excel file required.")

            return

        if not pdf:

            self.log("Please select a PDF file.")
            self.set_status("PDF file required.")

            return

        if not output:

            self.log("Please select an output folder.")
            self.set_status("Output folder required.")

            return

        self.settings["excel_file"] = excel
        self.settings["pdf_file"] = pdf
        self.settings["output_folder"] = output

        SettingsManager.save(self.settings)

        self.log("----------------------------------------")
        self.log("Matching process started.")
        self.log(f"Excel : {excel}")
        self.log(f"PDF    : {pdf}")
        self.log(f"Output : {output}")
        self.log("----------------------------------------")

        self.set_status("Matching...")

        try:

            self.matcher.start()

        except Exception as e:

            self.log(f"ERROR: {e}")

            self.set_status("Failed")

    # ==========================================================
    # Completion Dialog
    # ==========================================================

    def show_completion(self, result):

        try:

            CompletionDialog(

                self.root,

                result,

                self.output_entry.get().strip()

            )

        except Exception as e:

            self.log(f"Completion dialog error: {e}")

    # ==========================================================
    # Reset Dashboard
    # ==========================================================

    def reset_dashboard(self):

        self.update_progress(
            0,
            "Waiting..."
        )

        self.update_statistics(
            0,
            0,
            0,
            0
        )

        self.set_status("Ready")

    # ==========================================================
    # Enable / Disable Controls
    # ==========================================================

    def disable_controls(self):

        try:

            self.import_panel.start_btn.configure(
                state="disabled"
            )

            self.import_panel.clear_btn.configure(
                state="disabled"
            )

        except Exception:

            pass

    def enable_controls(self):

        try:

            self.import_panel.start_btn.configure(
                state="normal"
            )

            self.import_panel.clear_btn.configure(
                state="normal"
            )

        except Exception:

            pass

    # ==========================================================
    # Matching Callbacks
    # ==========================================================

    def matching_started(self):

        self.disable_controls()

        self.set_status(
            "Matching..."
        )

    def matching_finished(self):

        self.enable_controls()

        self.set_status(
            "Completed"
        )