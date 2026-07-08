"""
Matcher Controller
"""

from threading import Thread
from core.matcher_engine import run


class Matcher:

    def __init__(self, dashboard):
        self.dashboard = dashboard
        self.running = False

    def start(self):

        if self.running:
            return

        self.running = True

        Thread(
            target=self.run,
            daemon=True
        ).start()

    def stop(self):

        if not self.running:
            return

        self.running = False

        self.dashboard.log("Stopping process...")

        self.dashboard.set_status("Stopping...")

    def update_progress(self, value, message):

        self.dashboard.root.after(
            0,
            lambda: self.dashboard.progress_panel.update_progress(
                value,
                message
            )
        )

    def log(self, message):

        self.dashboard.root.after(
            0,
            lambda: self.dashboard.log(message)
        )

    def run(self):

        excel = self.dashboard.excel_entry.get().strip()
        pdf = self.dashboard.pdf_entry.get().strip()
        output = self.dashboard.output_entry.get().strip()

        if not excel:
            self.log("Please select an Excel file.")
            self.dashboard.set_status("No Excel selected")
            self.running = False
            return

        if not pdf:
            self.log("Please select a PDF file.")
            self.dashboard.set_status("No PDF selected")
            self.running = False
            return

        if not output:
            self.log("Please select an Output folder.")
            self.dashboard.set_status("No Output folder")
            self.running = False
            return

        self.dashboard.set_status("Processing...")

        self.log("===================================")
        self.log("LIMS Result Matcher Started")
        self.log("===================================")

        try:

            result = run(
                excel=excel,
                pdf=pdf,
                output=output,
                progress_callback=self.update_progress,
                log_callback=self.log,
                stop_callback=lambda: not self.running
            )

            self.update_progress(1.0, "Completed")

            self.dashboard.set_status("Completed")

            self.log("-----------------------------------")
            self.log("Processing Finished")
            self.log("-----------------------------------")
            self.log(f"Found: {result['found']}")
            self.log(f"Missing: {result['missing']}")
            self.log(f"Unreadable: {result['unreadable']}")

            self.dashboard.update_statistics(
    found=result["found"],
    missing=result["missing"],
    duplicate=0,
    unreadable=result["unreadable"]
)

            self.dashboard.root.after(
    0,
    lambda: self.dashboard.show_completion(result)
)


        except Exception as e:

            self.dashboard.set_status("Error")
            self.log(f"ERROR: {e}")

        finally:

            self.running = False