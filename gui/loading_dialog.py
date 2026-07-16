"""
Loading Dialog
HI Result Finder
"""

import customtkinter as ctk


class LoadingDialog(ctk.CTkToplevel):

    def __init__(self, master, message="Please wait..."):

        super().__init__(master)

        self.title("Working...")

        self.geometry("420x170")

        self.resizable(False, False)

        self.transient(master)

        self.grab_set()

        # Center on parent
        self.update_idletasks()

        x = master.winfo_rootx() + (master.winfo_width() // 2) - 210
        y = master.winfo_rooty() + (master.winfo_height() // 2) - 85

        self.geometry(f"+{x}+{y}")

        # Prevent closing
        self.protocol("WM_DELETE_WINDOW", lambda: None)

        # --------------------------------------------------

        title = ctk.CTkLabel(
            self,
            text="Please Wait",
            font=("Segoe UI", 20, "bold")
        )
        title.pack(pady=(20, 10))

        self.label = ctk.CTkLabel(
            self,
            text=message,
            font=("Segoe UI", 14)
        )
        self.label.pack()

        self.progress = ctk.CTkProgressBar(
            self,
            mode="indeterminate",
            width=320
        )

        self.progress.pack(pady=20)

        self.progress.start()

    # --------------------------------------------------

    def set_message(self, text):

        self.label.configure(text=text)
        self.update()

    # --------------------------------------------------

    def close(self):

        self.progress.stop()

        self.grab_release()

        self.destroy()