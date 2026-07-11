"""
Matcher Controller
Version 3.0.1
"""

import logging
import traceback
from threading import Thread
from tkinter import messagebox

from core.matcher_engine import run


class Matcher:

    def __init__(self, dashboard):

        self.dashboard = dashboard
        self.running = False

    # ======================================================
    # Start Thread
    # ======================================================

    def start(self):

        if self.running:

            logging.warning("Matcher is already running.")
            return

        logging.info("Creating matcher thread...")

        self.running = True

        Thread(
            target=self.run,
            daemon=True,
            name="MatcherThread"
        ).start()

    # ======================================================
    # Stop Thread
    # ======================================================

    def stop(self):

        if not self.running:
            return

        logging.info("Stopping matcher...")

        self.running = False

        self.dashboard.log("Stopping process...")

        self.dashboard.set_status("Stopping...")

    # ======================================================
    # Progress Update
    # ======================================================

    def update_progress(self, value, message):

        self.dashboard.root.after(
            0,
            lambda: self.dashboard.progress_panel.update_progress(
                value,
                message
            )
        )

    # ======================================================
    # Dashboard Log
    # ======================================================

    def log(self, message):

        logging.info(message)

        self.dashboard.root.after(
            0,
            lambda: self.dashboard.log(message)
        )

    # ======================================================
    # Main Matching Process
    # ======================================================

    def run(self):

        logging.info("=" * 70)
        logging.info("MATCHER THREAD STARTED")
        logging.info("=" * 70)

        try:

            excel = self.dashboard.excel_entry.get().strip()
            pdf = self.dashboard.pdf_entry.get().strip()
            output = self.dashboard.output_entry.get().strip()

            logging.info(f"Excel : {excel}")
            logging.info(f"PDF   : {pdf}")
            logging.info(f"Output: {output}")

            # ----------------------------------------------

            if not excel:

                self.log("Please select an Excel file.")
                self.dashboard.set_status("No Excel selected")
                logging.warning("Excel file not selected.")

                return

            if not pdf:

                self.log("Please select a PDF file.")
                self.dashboard.set_status("No PDF selected")
                logging.warning("PDF file not selected.")

                return

            if not output:

                self.log("Please select an Output folder.")
                self.dashboard.set_status("No Output folder")
                logging.warning("Output folder not selected.")

                return

            # ----------------------------------------------

            self.dashboard.set_status("Processing...")

            self.log("===================================")
            self.log("LIMS Result Matcher Started")
            self.log("===================================")

            logging.info("Calling matcher_engine.run()")

            result = run(
                excel=excel,
                pdf=pdf,
                output=output,
                progress_callback=self.update_progress,
                log_callback=self.log,
                stop_callback=lambda: not self.running
            )

            logging.info("matcher_engine.run() completed.")

            # ----------------------------------------------

            # Ensure result is a dict and provide defaults if run() returned None
            if result is None:
                result = {"found": 0, "missing": 0, "unreadable": 0}

            self.update_progress(1.0, "Completed")

            self.dashboard.set_status("Completed")

            self.log("-----------------------------------")
            self.log("Processing Finished")
            self.log("-----------------------------------")
            self.log(f"Found      : {result.get('found', 0)}")
            self.log(f"Missing    : {result.get('missing', 0)}")
            self.log(f"Unreadable : {result.get('unreadable', 0)}")

            logging.info(
                f"Summary -> "
                f"Found={result.get('found', 0)} | "
                f"Missing={result.get('missing', 0)} | "
                f"Unreadable={result.get('unreadable', 0)}"
            )

            self.dashboard.update_statistics(
                found=result.get("found", 0),
                missing=result.get("missing", 0),
                duplicate=0,
                unreadable=result.get("unreadable", 0)
            )

            self.dashboard.root.after(
                0,
                lambda: self.dashboard.show_completion(result)
            )

            logging.info("Completion dialog displayed.")

        except Exception as e:

            logging.exception("Unhandled exception inside Matcher.run()")
            traceback.print_exc()

            self.dashboard.set_status("Error")

            error_message = str(e)

            self.log(f"ERROR: {error_message}")

            self.dashboard.root.after(
                0,
                lambda: messagebox.showerror(
                    "Processing Error",
                    f"{error_message}\n\nSee logs/app.log for details."
                )
            )

        finally:

            self.running = False

            logging.info("Matcher thread finished.")
            logging.info("=" * 70)