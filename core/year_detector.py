"""
Year Detection Module

Scans a laboratory PDF and determines which Collection
Years are available.

Developer:
    Hamza Isah

Application:
    HI Result Finder
"""

from email.mime import text
import re

from pypdf import PdfReader


# ==========================================================
# Regular Expressions
# ==========================================================

COLLECTION_DATE_PATTERN = re.compile(
    r"Collection\s*Date\.?\s*[:\-]?\s*(\d{4})[-/]\d{2}[-/]\d{2}",
    re.IGNORECASE
)

RECEIVED_DATE_PATTERN = re.compile(
    r"DATE\s+RECIEVED\s+AT\s+PCR\s+LAB\s*(\d{4})[-/]\d{2}[-/]\d{2}",
    re.IGNORECASE
)


# ==========================================================
# Extract Year From Page
# ==========================================================

def extract_collection_year(text):
    """
    Returns the laboratory collection year for a page.

    Priority

        1. Collection Date

        2. Date Received at PCR Lab

    Returns

        "2026"

        "2025"

        etc.

        or None
    """

    if not text:
        return None

    match = COLLECTION_DATE_PATTERN.search(text)

    if match:
        return match.group(1)

    match = RECEIVED_DATE_PATTERN.search(text)

    if match:
        return match.group(1)

    return None


# ==========================================================
# Detect Available Years
# ==========================================================

def detect_available_years(pdf_file):
    """
    Returns a list of years found inside a PDF.

    Example

        ["2026", "2025", "2024"]
    """

    reader = PdfReader(pdf_file)

    years = set()

    for page in reader.pages:

        try:

            text = page.extract_text() or ""
            print("=" * 60)
            print(text[:600])
            print("=" * 60)

        except Exception:

            continue

        year = extract_collection_year(text)

        if year:

            years.add(year)

    return sorted(
        years,
        reverse=True
    )