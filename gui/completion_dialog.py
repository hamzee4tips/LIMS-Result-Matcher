import customtkinter as ctk
import os


class CompletionDialog(ctk.CTkToplevel):

    def __init__(self, parent, result, output_folder):

        super().__init__(parent)

        self.title("LIMS Result Matcher")

        self.geometry("500x420")

        self.resizable(False, False)

        self.grab_set()

        ctk.CTkLabel(
            self,
            text="✔ Matching Completed",
            font=("Segoe UI", 22, "bold")
        ).pack(pady=(20, 10))

        ctk.CTkLabel(
            self,
            text="LIMS Result Matcher\nDeveloper: Hamza Isah",
            justify="center"
        ).pack()

        ctk.CTkTextbox(
            self,
            width=430,
            height=170
        ).pack(pady=20)

        textbox = self.winfo_children()[-1]

        textbox.insert(
            "1.0",
            f"""
Processing completed successfully.

Found        : {result['found']}

Missing      : {result['missing']}

Unreadable   : {result['unreadable']}

Summary Report

{result['summary_report']}
"""
        )

        textbox.configure(state="disabled")

        ctk.CTkButton(
            self,
            text="📂 Open Output Folder",
            command=lambda: os.startfile(output_folder)
        ).pack(pady=8)

        ctk.CTkButton(
            self,
            text="Close",
            command=self.destroy
        ).pack(pady=8)