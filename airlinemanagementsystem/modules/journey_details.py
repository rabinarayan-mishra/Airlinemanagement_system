import tkinter as tk
from tkinter import ttk
from db import connect_db


class JourneyDetails:

    def __init__(self, parent):

        parent.configure(bg="#F4F7FC")

        # ---------------- Title ---------------- #

        title_row = tk.Frame(parent, bg="#F4F7FC")
        title_row.pack(pady=(20, 5))

        tk.Label(
            title_row,
            text="🧾",
            font=("Segoe UI", 40),
            bg="#F4F7FC",
            fg="#1E3A8A"
        ).pack(side=tk.LEFT, padx=(0, 12))

        tk.Label(
            title_row,
            text="JOURNEY DETAILS",
            font=("Segoe UI", 24, "bold"),
            bg="#F4F7FC",
            fg="#1E3A8A"
        ).pack(side=tk.LEFT)

        tk.Label(
            parent,
            text="All bookings made through the system",
            font=("Segoe UI", 11),
            bg="#F4F7FC",
            fg="#64748B"
        ).pack()

        # ---------------- Toolbar ---------------- #

        toolbar = tk.Frame(parent, bg="#F4F7FC")
        toolbar.pack(fill=tk.X, padx=40, pady=(15, 5))

        self.count_label = tk.Label(
            toolbar,
            text="",
            font=("Segoe UI", 10, "bold"),
            bg="#F4F7FC",
            fg="#334155"
        )
        self.count_label.pack(side=tk.LEFT)

        self._make_button(
            toolbar,
            text="🔄  Refresh",
            command=self.load_data,
            bg="#2563EB"
        ).pack(side=tk.RIGHT)

        # ---------------- Card ---------------- #

        card = tk.Frame(
            parent,
            bg="white",
            highlightbackground="#D1D5DB",
            highlightthickness=1,
            bd=0
        )

        card.pack(fill=tk.BOTH, expand=True, padx=40, pady=(5, 30))

        table_frame = tk.Frame(card, bg="white")
        table_frame.pack(fill=tk.BOTH, expand=True, padx=15, pady=15)

        # ---------------- Treeview Style ---------------- #

        style = ttk.Style()
        style.theme_use("clam")

        style.configure(
            "Airline.Treeview",
            font=("Segoe UI", 10),
            rowheight=34,
            background="white",
            fieldbackground="white",
            foreground="#1f2937",
            borderwidth=0
        )

        style.configure(
            "Airline.Treeview.Heading",
            font=("Segoe UI", 10, "bold"),
            background="#1E3A8A",
            foreground="white",
            relief="flat",
            padding=8
        )

        style.map(
            "Airline.Treeview.Heading",
            background=[("active", "#1E40AF")]
        )

        style.map(
            "Airline.Treeview",
            background=[("selected", "#DBEAFE")],
            foreground=[("selected", "#1E3A8A")]
        )

        style.configure(
            "Airline.Vertical.TScrollbar",
            background="#CBD5E1",
            troughcolor="white",
            bordercolor="white",
            arrowcolor="#334155",
            relief="flat"
        )

        cols = (
            "PNR",
            "Passenger ID",
            "Flight ID",
            "Seats",
            "Price",
            "Status",
            "Booking Date"
        )

        col_widths = {
            "PNR": 120,
            "Passenger ID": 110,
            "Flight ID": 90,
            "Seats": 70,
            "Price": 110,
            "Status": 120,
            "Booking Date": 170
        }

        self.tree = ttk.Treeview(
            table_frame,
            columns=cols,
            show="headings",
            height=15,
            style="Airline.Treeview"
        )

        for c in cols:
            self.tree.heading(c, text=c)
            self.tree.column(
                c,
                width=col_widths.get(c, 130),
                anchor="center"
            )

        # Alternating row colors + status color tags
        self.tree.tag_configure("evenrow", background="#F8FAFC")
        self.tree.tag_configure("oddrow", background="white")
        self.tree.tag_configure("confirmed", foreground="#16A34A")
        self.tree.tag_configure("cancelled", foreground="#DC2626")

        scrollbar = ttk.Scrollbar(
            table_frame,
            orient="vertical",
            command=self.tree.yview,
            style="Airline.Vertical.TScrollbar"
        )

        self.tree.configure(yscrollcommand=scrollbar.set)

        self.tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

        self.parent = parent
        self.load_data()

    # ------------------------------------------------------------------ #
    # Custom "button" built from a Label — native tk.Button ignores the
    # bg color on macOS, so a styled Label with click/hover bindings is
    # used instead to guarantee consistent colors cross-platform.
    # ------------------------------------------------------------------ #
    def _make_button(self, parent, text, command, bg, fg="white",
                      font=("Segoe UI", 10, "bold"), padx=15, pady=6):

        btn = tk.Label(
            parent,
            text=text,
            bg=bg,
            fg=fg,
            font=font,
            padx=padx,
            pady=pady,
            cursor="hand2",
            relief="flat"
        )

        def on_enter(e):
            btn.config(bg=self._darken(bg))

        def on_leave(e):
            btn.config(bg=bg)

        def on_click(e):
            command()

        btn.bind("<Enter>", on_enter)
        btn.bind("<Leave>", on_leave)
        btn.bind("<Button-1>", on_click)

        return btn

    @staticmethod
    def _darken(hex_color, factor=0.85):
        hex_color = hex_color.lstrip("#")
        r, g, b = (int(hex_color[i:i + 2], 16) for i in (0, 2, 4))
        r, g, b = (max(0, int(c * factor)) for c in (r, g, b))
        return f"#{r:02x}{g:02x}{b:02x}"

    def load_data(self):

        for row in self.tree.get_children():
            self.tree.delete(row)

        try:

            conn = connect_db()
            cur = conn.cursor()

            cur.execute("""
                SELECT pnr,
                       passenger_id,
                       flight_id,
                       seats,
                       total_price,
                       status,
                       booking_date
                FROM bookings
                ORDER BY booking_date DESC
            """)

            records = cur.fetchall()

            conn.close()

            for i, row in enumerate(records):

                row = list(row)
                row[4] = f"₹{row[4]:,.2f}"

                stripe_tag = "evenrow" if i % 2 == 0 else "oddrow"
                status_tag = (
                    "confirmed" if str(row[5]).upper() == "CONFIRMED"
                    else "cancelled"
                )

                self.tree.insert(
                    "",
                    tk.END,
                    values=row,
                    tags=(stripe_tag, status_tag)
                )

            self.count_label.config(
                text=f"{len(records)} booking(s) found"
            )

        except Exception as e:

            self.count_label.config(
                text=f"Database Error: {str(e)}",
                fg="#DC2626"
            )