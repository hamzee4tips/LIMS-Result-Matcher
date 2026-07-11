"""
Application Settings Manager
HI Result Finder v3.0.1
"""

import json
import os
from pathlib import Path


# ==========================================================
# Application Folder
# ==========================================================

APP_NAME = "HI Result Finder"

LOCAL_APPDATA = os.getenv("LOCALAPPDATA")

if LOCAL_APPDATA:

    APP_FOLDER = Path(LOCAL_APPDATA) / APP_NAME

else:

    APP_FOLDER = Path.home() / APP_NAME


APP_FOLDER.mkdir(
    parents=True,
    exist_ok=True
)


SETTINGS_FILE = APP_FOLDER / "settings.json"


DEFAULT_SETTINGS = {

    "excel_file": "",

    "pdf_file": "",

    "output_folder": "",

    "theme": "dark"

}


# ==========================================================
# Settings Manager
# ==========================================================

class SettingsManager:


    @staticmethod
    def load():

        if not SETTINGS_FILE.exists():

            SettingsManager.save(DEFAULT_SETTINGS)

            return DEFAULT_SETTINGS.copy()

        try:

            with open(
                SETTINGS_FILE,
                "r",
                encoding="utf-8"
            ) as f:

                data = json.load(f)

        except Exception:

            SettingsManager.save(DEFAULT_SETTINGS)

            return DEFAULT_SETTINGS.copy()

        settings = DEFAULT_SETTINGS.copy()

        settings.update(data)

        return settings


    @staticmethod
    def save(settings):

        SETTINGS_FILE.parent.mkdir(
            parents=True,
            exist_ok=True
        )

        with open(
            SETTINGS_FILE,
            "w",
            encoding="utf-8"
        ) as f:

            json.dump(
                settings,
                f,
                indent=4
            )