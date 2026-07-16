"""
File Selector
HI Result Finder v3.1
"""

import threading

from tkinter import filedialog

from core.settings import SettingsManager
from core.year_detector import detect_available_years

from gui.loading_dialog import LoadingDialog


class FileSelector:

    # ======================================================
    # Constructor
    # ======================================================

    def __init__(self, dashboard):

        self.dashboard = dashboard

        self.settings = SettingsManager.load()

    # ======================================================
    # Background Year Scan
    # ======================================================

    def _scan_pdf_years(self, filename, loading):

        try:

            years = detect_available_years(filename)

            self.dashboard.root.after(
                0,
                lambda: self._finish_year_scan(
                    years,
                    loading
                )
            )

        except Exception as e:

            self.dashboard.root.after(
                0,
                lambda: self._year_scan_failed(
                    e,
                    loading
                )
            )

    # ======================================================
    # Scan Finished
    # ======================================================

    def _finish_year_scan(self, years, loading):

        loading.close()

        self.dashboard.available_years = years

        values = ["All Years"] + years

        self.dashboard.import_panel.year_combo.configure(
            values=values
        )

        self.dashboard.search_year.set("All Years")

        if years:

            self.dashboard.log(
                f"Detected Years: {', '.join(years)}"
            )

        else:

            self.dashboard.log(
                "No Collection Years detected."
            )

    # ======================================================
    # Scan Failed
    # ======================================================

    def _year_scan_failed(self, error, loading):

        loading.close()

        self.dashboard.log(
            f"Year Detection Failed: {error}"
        )

    # ======================================================
    # Browse Excel
    # ======================================================

    def browse_excel(self, entry):

        filename = filedialog.askopenfilename(

            title="Select Excel File",

            filetypes=[
                ("Excel Files", "*.xlsx *.xls"),
                ("All Files", "*.*")
            ]

        )

        if not filename:
            return

        entry.delete(0, "end")
        entry.insert(0, filename)

        self.settings["excel_file"] = filename

        SettingsManager.save(
            self.settings
        )
            # ======================================================
    # Browse PDF
    # ======================================================

    def browse_pdf(self, entry):

        filename = filedialog.askopenfilename(

            title="Select PDF File",

            filetypes=[
                ("PDF Files", "*.pdf"),
                ("All Files", "*.*")
            ]

        )

        if not filename:
            return

        # ----------------------------------------------

        entry.delete(0, "end")
        entry.insert(0, filename)

        self.settings["pdf_file"] = filename

        SettingsManager.save(
            self.settings
        )

        # ----------------------------------------------
        # Show Loading Dialog
        # ----------------------------------------------

        loading = LoadingDialog(

            self.dashboard.root,

            "Scanning PDF for available years...\n\n"
            "Please wait until the scan is completed."

        )

        # Allow dialog to paint before starting thread
        self.dashboard.root.update_idletasks()

        # ----------------------------------------------
        # Background Scan
        # ----------------------------------------------

        threading.Thread(

            target=self._scan_pdf_years,

            args=(
                filename,
                loading
            ),

            daemon=True

        ).start()

    # ======================================================
    # Browse Output Folder
    # ======================================================

    def browse_output(self, entry):

        folder = filedialog.askdirectory(

            title="Select Output Folder"

        )

        if not folder:
            return

        entry.delete(0, "end")
        entry.insert(0, folder)

        self.settings["output_folder"] = folder

        SettingsManager.save(
            self.settings
        )