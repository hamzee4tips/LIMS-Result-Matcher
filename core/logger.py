"""
Application Logger
HI Result Finder v3.0.1
"""

import logging
import os
from pathlib import Path


# ==========================================================
# Application Data Folder
# ==========================================================

APP_NAME = "HI Result Finder"

LOCAL_APPDATA = os.getenv("LOCALAPPDATA")

if LOCAL_APPDATA:

    APP_FOLDER = Path(LOCAL_APPDATA) / APP_NAME

else:

    APP_FOLDER = Path.home() / APP_NAME


LOG_FOLDER = APP_FOLDER / "logs"

LOG_FOLDER.mkdir(
    parents=True,
    exist_ok=True
)

LOG_FILE = LOG_FOLDER / "app.log"


# ==========================================================
# Logger Setup
# ==========================================================

def setup_logger():

    logging.basicConfig(

        level=logging.INFO,

        format="%(asctime)s | %(levelname)s | %(message)s",

        handlers=[

            logging.FileHandler(
                LOG_FILE,
                encoding="utf-8"
            ),

            logging.StreamHandler()

        ]

    )

    logging.info("=" * 70)
    logging.info("HI Result Finder started")
    logging.info("=" * 70)

    logging.info(f"Log Folder : {LOG_FOLDER}")
    logging.info(f"Log File   : {LOG_FILE}")