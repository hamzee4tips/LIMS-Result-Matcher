"""
Application Settings Manager
"""

import json
import os

SETTINGS_FILE = os.path.join("config", "settings.json")


class SettingsManager:

    @staticmethod
    def load():

        if not os.path.exists(SETTINGS_FILE):
            return {
                "excel_file": "",
                "pdf_file": "",
                "output_folder": "",
                "theme": "dark"
            }

        with open(SETTINGS_FILE, "r") as f:
            return json.load(f)

    @staticmethod
    def save(settings):

        with open(SETTINGS_FILE, "w") as f:
            json.dump(settings, f, indent=4)