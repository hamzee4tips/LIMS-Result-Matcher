"""
Resource Manager
HI Result Finder v3.0.1

Provides the correct path to application resources
for both Development and PyInstaller builds.
"""

import os
import sys
from pathlib import Path


# ==========================================================
# Base Resource Folder
# ==========================================================

def application_path() -> Path:
    """
    Returns the application root folder.

    Development:
        Project Root

    PyInstaller:
        _MEIPASS temporary extraction folder
    """

    if getattr(sys, "frozen", False):

        return Path(getattr(sys, "_MEIPASS"))

    return Path(__file__).resolve().parent.parent


# ==========================================================
# Resource Path
# ==========================================================

def resource_path(relative_path: str) -> str:
    """
    Returns the absolute path to a bundled resource.

    Example:

    resource_path("assets/images/logo.png")
    """

    return str(application_path() / relative_path)


# ==========================================================
# Helpers
# ==========================================================

def resource_exists(relative_path: str) -> bool:

    return os.path.exists(resource_path(relative_path))


def image_path(filename: str) -> str:

    return resource_path(f"assets/images/{filename}")


def icon_path(filename: str) -> str:

    return resource_path(f"assets/icons/{filename}")


def config_path(filename: str) -> str:

    return resource_path(f"config/{filename}")