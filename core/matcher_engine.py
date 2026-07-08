"""
LIMS Result Matcher Engine
Developer: Hamza Isah

Refactored from Version 2.0
"""

import logging
import re
from pathlib import Path

import pandas as pd
from pypdf import PdfReader, PdfWriter


# ===========================================================
# Utility Functions
# ===========================================================

def norm(value):
    """Normalize PepID"""
    return re.sub(r"\s+", "", str(value)).upper()


def safe(value):
    """Safe filename"""
    return re.sub(r'[<>:"/\\\\|?*]+', "_", str(value))


PATTERNS = [

    re.compile(
        r"ID\s*[:\-]?\s*(.*?)\s*Client'?s?\s*Unique\s*Number",
        re.I | re.S
    ),

    re.compile(
        r"ID\s+([A-Z0-9/]+)",
        re.I
    ),

    re.compile(
        r"([A-Z]{2,10}(?:/[A-Z0-9]+)+/\d{2,})",
        re.I
    )

]


def extract(text):

    text = text or ""

    for pattern in PATTERNS:

        match = pattern.search(text)

        if match:

            return norm(match.group(1))

    return None


# ===========================================================
# Excel Loader
# ===========================================================

def load_pending(
        excel,
        sheet,
        id_column,
        person_column
):

    df = pd.read_excel(
        excel,
        sheet_name=sheet if sheet else 0
    )

    cols = {
        c.lower(): c
        for c in df.columns
    }

    id_column = cols.get(
        id_column.lower(),
        id_column
    )

    person_column = cols.get(
        person_column.lower(),
        person_column
    )

    pending = {}

    for _, row in df.iterrows():

        if pd.isna(row[id_column]):
            continue

        pepid = norm(row[id_column])

        person = str(
            row.get(person_column, "UNKNOWN")
        ).strip()

        if not person:
            person = "UNKNOWN"

        pending[pepid] = person

    return pending


# ===========================================================
# Main Engine
# ===========================================================

def run(

        excel,

        pdf,

        output,

        sheet=None,

        id_column="PepID",

        person_column="Person responsible",

        debug=False,

        progress_callback=None,

        log_callback=None,

        stop_callback=None

):

    output = Path(output)

    output.mkdir(
        parents=True,
        exist_ok=True
    )

    logging.basicConfig(

        filename=output / "Processing_Log.txt",

        level=logging.INFO,

        filemode="w"

    )

    pending = load_pending(

        excel,

        sheet,

        id_column,

        person_column

    )

    reader = PdfReader(pdf)

    total_pages = len(reader.pages)

    found = {}

    unreadable = []

    summary = {}

    if log_callback:
        log_callback(f"Loaded {len(pending)} pending IDs.")

    if log_callback:
        log_callback(f"Scanning {total_pages} pages...")
            # ===========================================================
    # Scan PDF
    # ===========================================================

    for page_number, page in enumerate(reader.pages, start=1):

        if stop_callback and stop_callback():

            if log_callback:
                log_callback("Processing cancelled.")

            return {
                "found": len(found),
                "missing": len(pending) - len(found),
                "unreadable": len(unreadable)
            }

        if progress_callback:

            progress_callback(
                page_number / total_pages,
                f"Scanning page {page_number} of {total_pages}"
            )

        try:

            text = page.extract_text() or ""

        except Exception:

            unreadable.append(page_number)

            continue

        pepid = extract(text)

        if debug:

            logging.info(
                "Page %s -> %s",
                page_number,
                pepid
            )

        if not pepid:

            unreadable.append(page_number)

            continue

        if pepid not in pending:

            continue

        found.setdefault(
            pepid,
            []
        ).append(page_number)

    if log_callback:

        log_callback(
            f"Matched {len(found)} IDs."
        )

    # ===========================================================
    # Export Individual PDFs
    # ===========================================================

    for pepid, pages in found.items():

        person = pending[pepid]

        summary.setdefault(
            person,
            [0, 0]
        )

        summary[person][1] += 1

        folder = output / safe(person)

        folder.mkdir(
            parents=True,
            exist_ok=True
        )

        writer = PdfWriter()

        for page in pages:

            writer.add_page(
                reader.pages[page - 1]
            )

        with open(
            folder / f"{safe(pepid)}.pdf",
            "wb"
        ) as fp:

            writer.write(fp)

    if log_callback:

        log_callback(
            "PDF extraction completed."
        )
            # ===========================================================
    # Build Reports
    # ===========================================================

    missing = []

    for pepid, person in pending.items():

        if pepid not in found:

            missing.append({
                "PepID": pepid,
                "Person Responsible": person
            })

        summary.setdefault(
            person,
            [0, 0]
        )

        summary[person][0] += 1

    # -----------------------------
    # Summary Report
    # -----------------------------

    summary_rows = []

    for person in sorted(summary):

        total = summary[person][0]

        matched = summary[person][1]

        summary_rows.append({

            "Person Responsible": person,

            "Pending IDs": total,

            "Found": matched,

            "Missing": total - matched,

            "Completion %": round(
                (matched / total * 100),
                2
            ) if total else 0

        })

    pd.DataFrame(
        summary_rows
    ).to_excel(

        output / "Summary_Report.xlsx",

        index=False

    )

    # -----------------------------
    # Missing Report
    # -----------------------------

    pd.DataFrame(
        missing
    ).to_excel(

        output / "Missing_Report.xlsx",

        index=False

    )

    # -----------------------------
    # Unreadable Pages
    # -----------------------------

    pd.DataFrame({

        "Unreadable Page": unreadable

    }).to_excel(

        output / "Unreadable_Pages.xlsx",

        index=False

    )

    # -----------------------------
    # Found Report
    # -----------------------------

    found_rows = []

    for pepid, pages in found.items():

        found_rows.append({

            "PepID": pepid,

            "Person Responsible": pending[pepid],

            "Pages": ", ".join(
                str(x) for x in pages
            ),

            "PDF File": str(
                output /
                safe(pending[pepid]) /
                f"{safe(pepid)}.pdf"
            )

        })

    pd.DataFrame(
        found_rows
    ).to_excel(

        output / "Found_Report.xlsx",

        index=False

    )

    # ===========================================================
    # Finish
    # ===========================================================

    if progress_callback:

        progress_callback(
            1.0,
            "Completed"
        )

    if log_callback:

        log_callback("")
        log_callback("====================================")
        log_callback("Processing Completed")
        log_callback("====================================")
        log_callback(f"Pending IDs : {len(pending)}")
        log_callback(f"Found       : {len(found)}")
        log_callback(f"Missing     : {len(missing)}")
        log_callback(f"Unreadable  : {len(unreadable)}")

    logging.info("Processing completed successfully.")

    return {

        "found": len(found),

        "missing": len(missing),

        "unreadable": len(unreadable),

        "summary_report": str(
            output / "Summary_Report.xlsx"
        ),

        "missing_report": str(
            output / "Missing_Report.xlsx"
        ),

        "found_report": str(
            output / "Found_Report.xlsx"
        ),

        "unreadable_report": str(
            output / "Unreadable_Pages.xlsx"
        )

    }