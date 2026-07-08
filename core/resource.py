import os
import sys


def resource_path(relative_path: str) -> str:
    """
    Returns the correct path for resources in both
    development and PyInstaller builds.
    """

    if getattr(sys, "frozen", False):
        base_path = getattr(sys, "_MEIPASS", os.path.dirname(sys.executable))
    else:
        base_path = os.path.dirname(os.path.abspath(__file__))
        base_path = os.path.dirname(base_path)

    return os.path.join(base_path, relative_path)