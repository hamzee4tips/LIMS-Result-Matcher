"""
File Selector
"""

import customtkinter as ctk
from tkinter import filedialog

from core.settings import SettingsManager


class FileSelector:

    def __init__(self):

        self.settings = SettingsManager.load()

    def browse_excel(self, entry):

        filename = filedialog.askopenfilename(
            title="Select Excel File",
            filetypes=[
                ("Excel Files", "*.xlsx *.xls"),
                ("All Files", "*.*")
            ]
        )

        if filename:

            entry.delete(0, "end")
            entry.insert(0, filename)

            self.settings["excel_file"] = filename
            SettingsManager.save(self.settings)

    def browse_pdf(self, entry):

        filename = filedialog.askopenfilename(
            title="Select PDF File",
            filetypes=[
                ("PDF Files", "*.pdf"),
                ("All Files", "*.*")
            ]
        )

        if filename:

            entry.delete(0, "end")
            entry.insert(0, filename)

            self.settings["pdf_file"] = filename
            SettingsManager.save(self.settings)

    def browse_output(self, entry):

        folder = filedialog.askdirectory(
            title="Select Output Folder"
        )

        if folder:

            entry.delete(0, "end")
            entry.insert(0, folder)

            self.settings["output_folder"] = folder
            SettingsManager.save(self.settings)