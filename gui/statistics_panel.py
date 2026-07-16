"""
Statistics Panel
HI Result Finder v3.1
"""

import customtkinter as ctk


class StatisticCard(ctk.CTkFrame):

    def __init__(self, master, title):

        super().__init__(
            master,
            corner_radius=10
        )

        self.value = ctk.CTkLabel(
            self,
            text="0",
            font=("Segoe UI", 28, "bold")
        )

        self.value.pack(
            pady=(15, 5)
        )

        ctk.CTkLabel(
            self,
            text=title,
            font=("Segoe UI", 12)
        ).pack(
            pady=(0, 15)
        )

    def set(self, value):

        self.value.configure(
            text=str(value)
        )


class StatisticsPanel(ctk.CTkFrame):

    def __init__(self, master):

        super().__init__(
            master,
            corner_radius=12
        )

        ctk.CTkLabel(
            self,
            text="Statistics",
            font=("Segoe UI", 18, "bold")
        ).pack(
            anchor="w",
            padx=20,
            pady=(15, 10)
        )

        cards = ctk.CTkFrame(
            self,
            fg_color="transparent"
        )

        cards.pack(
            fill="x",
            padx=15,
            pady=(0, 15)
        )

        self.found = StatisticCard(cards, "Found")
        self.found.pack(side="left", expand=True, fill="x", padx=5)

        self.missing = StatisticCard(cards, "Missing")
        self.missing.pack(side="left", expand=True, fill="x", padx=5)
        self.duplicate = StatisticCard(cards, "Duplicate")

        self.duplicate.pack(
            side="left",
            expand=True,
            fill="x",
            padx=5
   )
        self.unreadable = StatisticCard(cards, "Unreadable")
        self.unreadable.pack(side="left", expand=True, fill="x", padx=5)

    def update(
        self,
        found,
        missing,
        duplicate,
        unreadable
    ):

        self.found.set(found)
        self.missing.set(missing)
        self.duplicate.set(duplicate)
        self.unreadable.set(unreadable)

    def reset(self):

        self.update(
            0,
            0,
            0,
            0
)