"""
HI Result Finder
Dashboard Controller

Version : 3.1.0
Developer : Hamza Isah

The Dashboard acts as the controller for the application.
It coordinates all UI components and backend services.

No other class should manipulate another class directly.
Everything is routed through Dashboard.
"""

import logging
import customtkinter as ctk
from gui.statistics_panel import StatisticsPanel
from gui.progress_panel import ProgressPanel
from tkinter import messagebox
from version import *

from core.settings import SettingsManager
from core.logger import setup_logger

from core.matcher import Matcher
from gui.file_selector import FileSelector
from gui.import_panel import ImportPanel

WINDOW_WIDTH = 1400
WINDOW_HEIGHT = 850

# (Will be added in Part 2)
# from gui.loading_popup import LoadingPopup


class Dashboard:

    # ==========================================================
    # Constructor
    # ==========================================================

    def __init__(self, root):

        self.root = root

        # ------------------------------------------------------
        # Settings
        # ------------------------------------------------------

        self.settings = SettingsManager.load()

        self.search_year = ctk.StringVar(
            value=self.settings.get(
                "search_year",
                "All Years"
            )
        )

        self.available_years = []

        # ------------------------------------------------------
        # Logging
        # ------------------------------------------------------

        setup_logger()

        logging.info("=" * 70)
        logging.info("Creating Dashboard")
        logging.info("=" * 70)

        # ------------------------------------------------------
        # Window
        # ------------------------------------------------------

        self.root.title(APP_NAME)

        self.root.geometry(("1400x850"))

        self.root.minsize(
            1250,
            760
        )

        # ------------------------------------------------------
        # Theme
        # ------------------------------------------------------

        ctk.set_appearance_mode(
            self.settings.get(
                "theme",
                "dark"
            )
        )

        # ------------------------------------------------------
        # Runtime Objects
        # ------------------------------------------------------

        self.loading_popup = None

        self.selector = FileSelector(self)

        self.matcher = Matcher(self)

        # ------------------------------------------------------
        # Runtime Variables
        # ------------------------------------------------------

        self.excel_entry = None

        self.pdf_entry = None

        self.output_entry = None

        self.import_panel = None

        self.status_label = None

        self.log_box = None

        self.progress_bar = None

        # ------------------------------------------------------
        # Build Interface
        # ------------------------------------------------------

        self.build_interface()

        logging.info("Dashboard created successfully.")
        # ==========================================================
        # Build Interface
        # ==========================================================

    def build_interface(self):

        logging.info("=" * 70)
        logging.info("Building Dashboard Interface")
        logging.info("=" * 70)

        # ------------------------------------------------------
        # Main Container
        # ------------------------------------------------------

        self.main_frame = ctk.CTkFrame(
            self.root,
            corner_radius=0
        )

        self.main_frame.pack(
            fill="both",
            expand=True
        )

        # ------------------------------------------------------
        # Left Panel
        # ------------------------------------------------------

        self.left_panel = ctk.CTkFrame(
            self.main_frame,
            width=430,
            corner_radius=0
        )

        self.left_panel.pack(
            side="left",
            fill="y"
        )

        self.left_panel.pack_propagate(False)

        # ------------------------------------------------------
        # Right Panel
        # ------------------------------------------------------

        self.right_panel = ctk.CTkFrame(
            self.main_frame,
            corner_radius=0
        )

        self.right_panel.pack(
            side="right",
            fill="both",
            expand=True
        )

        # ------------------------------------------------------
        # Import Panel
        # ------------------------------------------------------

        self.import_panel = ImportPanel(
            self.left_panel,
            self
        )

        self.import_panel.pack(
            fill="x",
            padx=15,
            pady=15
        )


        # ------------------------------------------------------
        # Activity Log Header
        # ------------------------------------------------------

        header = ctk.CTkLabel(
            self.right_panel,
            text="Activity Log",
            font=("Segoe UI", 20, "bold")
        )

        header.pack(
            anchor="w",
            padx=20,
            pady=(20, 10)
        )

        # ------------------------------------------------------
        # Log Window
        # ------------------------------------------------------

        self.log_box = ctk.CTkTextbox(
            self.right_panel,
            wrap="word",
            font=("Consolas", 12)
        )

        self.log_box.pack(
            fill="both",
            expand=True,
            padx=20,
            pady=(0, 15)
        )

        self.log_box.configure(
            state="disabled"
        )

        # ------------------------------------------------------
        # Progress Bar
        # ------------------------------------------------------

        self.progress_bar = ctk.CTkProgressBar(
            self.right_panel
        )

        self.progress_bar.pack(
            fill="x",
            padx=20,
            pady=(0, 10)
        )

        self.progress_bar.set(0)

        # ------------------------------------------------------
        # Status Bar
        # ------------------------------------------------------

        status_frame = ctk.CTkFrame(
            self.right_panel,
            height=35,
            corner_radius=8
        )

        status_frame.pack(
            fill="x",
            padx=20,
            pady=(0, 20)
        )

        self.status_label = ctk.CTkLabel(
            status_frame,
            text="Ready",
            anchor="w"
        )

        self.status_label.pack(
            side="left",
            padx=15,
            pady=8
        )

        logging.info("Dashboard interface created.")

    # ==========================================================
    # Progress Panel
    # ==========================================================

        self.progress_panel = ProgressPanel(self.right_panel)

        self.progress_panel.pack(
            fill="x",
            padx=15,
            pady=(15, 10)
        )

    # ==========================================================
    # Statistics Panel
    # ==========================================================

        self.statistics_panel = StatisticsPanel(
        self.right_panel
        )

        self.statistics_panel.pack(
    fill="x",
    padx=15,
    pady=(0, 10)
)
    # ==========================================================
    # Activity Log
    # ==========================================================

    def log(self, message):

        logging.info(message)

        if self.log_box is None:
            return

        self.log_box.configure(state="normal")

        self.log_box.insert(
            "end",
            f"{message}\n"
        )

        self.log_box.see("end")

        self.log_box.configure(state="disabled")

        self.root.update_idletasks()

    # ==========================================================
    # Status
    # ==========================================================

    def set_status(self, message):

        if self.status_label:

            self.status_label.configure(
                text=message
            )

        self.root.update_idletasks()

    # ==========================================================
    # Progress
    # ==========================================================

    def set_progress(self, value):

        if self.progress_bar:

            value = max(
                0,
                min(1, value)
            )

            self.progress_bar.set(value)

        self.root.update_idletasks()
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

        self.statistics_panel.update(
        found,
        missing,
        duplicate,
        unreadable
            )

        self.root.update_idletasks()

    # ==========================================================
    # Year List
    # ==========================================================

    def update_year_list(self, years):

        self.available_years = years

        values = ["All Years"] + years

        self.import_panel.year_combo.configure(
            values=values
        )

        self.import_panel.year_combo.set(
            "All Years"
        )

        self.search_year.set(
            "All Years"
        )

        self.settings["search_year"] = "All Years"

        SettingsManager.save(
            self.settings
        )

        if years:

            self.log(
                "Detected Collection Years: "
                + ", ".join(years)
            )

        else:

            self.log(
                "No collection years detected."
            )

    # ==========================================================
    # Loading Popup
    # ==========================================================

    def show_loading_popup(
        self,
        title="Please wait...",
        message="Processing..."
    ):

        # LoadingPopup will be added in Phase 2.
        # Placeholder for now.

        self.set_status(message)

        self.log(message)

    def hide_loading_popup(self):

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
    # Start Matching
    # ==========================================================

    def start_matching(self):

        self.disable_controls()

        self.set_progress(0)

        self.set_status(
            "Starting matcher..."
        )

        self.log(
            "Starting matching process..."
        )

        self.matcher.start()

    # ==========================================================
    # Matching Finished
    # ==========================================================

    def matching_finished(
        self,
        found,
        missing,
        unreadable
    ):

        self.enable_controls()

        self.set_progress(1)

        self.set_status(
            "Completed"
        )

        self.log("")

        self.log("=" * 45)

        self.log("Processing Completed")

        self.log("=" * 45)

        self.log(f"Found      : {found}")

        self.log(f"Missing    : {missing}")

        self.log(f"Unreadable : {unreadable}")

        messagebox.showinfo(

            "HI Result Finder",

            (
                "Processing Completed Successfully.\n\n"
                f"Found: {found}\n"
                f"Missing: {missing}\n"
                f"Unreadable: {unreadable}"
            )

        )

    # ==========================================================
    # Shutdown
    # ==========================================================

    def shutdown(self):

        logging.info("Application Closed")

        self.root.destroy()