from tkinter import *
from tkinter import messagebox
from db import connect_db


def _make_button(parent, text, command, bg, fg="white",
                  font=("Segoe UI", 10, "bold"), padx=18, pady=8):
    """
    Custom "button" built from a Label.

    Native tk.Button ignores the bg color on macOS (Aqua theme), which
    makes colored buttons render as blank white boxes. A styled Label
    bound to click/hover events guarantees the colors render correctly
    on macOS, Windows, and Linux.
    """

    def darken(hex_color, factor=0.85):
        hex_color = hex_color.lstrip("#")
        r, g, b = (int(hex_color[i:i + 2], 16) for i in (0, 2, 4))
        r, g, b = (max(0, int(c * factor)) for c in (r, g, b))
        return f"#{r:02x}{g:02x}{b:02x}"

    btn = Label(
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

    btn.bind("<Enter>", lambda e: btn.config(bg=darken(bg)))
    btn.bind("<Leave>", lambda e: btn.config(bg=bg))
    btn.bind("<Button-1>", lambda e: command())

    return btn


class CancelTicket:

    STATUS_COLORS = {
        "CONFIRMED": "#16A34A",
        "CANCELLED": "#DC2626",
    }

    def __init__(self, parent):

        self.parent = parent
        parent.configure(bg="#F4F7FC")

        self.current_pnr = None
        self.current_status = None

        # ---------------- Title ---------------- #

        title_row = Frame(parent, bg="#F4F7FC")
        title_row.pack(pady=(20, 5))

        Label(
            title_row,
            text="🗑",
            font=("Segoe UI", 40),
            bg="#F4F7FC",
            fg="#1E3A8A"
        ).pack(side=LEFT, padx=(0, 12))

        Label(
            title_row,
            text="CANCEL TICKET",
            font=("Segoe UI", 24, "bold"),
            bg="#F4F7FC",
            fg="#1E3A8A"
        ).pack(side=LEFT)

        Label(
            parent,
            text="Look up a booking by PNR and cancel it",
            font=("Segoe UI", 11),
            bg="#F4F7FC",
            fg="#64748B"
        ).pack()

        # ---------------- Search Card ---------------- #

        search_card = Frame(
            parent,
            bg="white",
            highlightbackground="#D1D5DB",
            highlightthickness=1,
            bd=0
        )
        search_card.pack(pady=25)

        Label(
            search_card,
            text="🔎 Enter PNR",
            bg="white",
            fg="#334155",
            font=("Segoe UI", 11, "bold")
        ).grid(row=0, column=0, sticky="w", padx=20, pady=15)

        self.pnr_entry = Entry(
            search_card,
            width=25,
            font=("Segoe UI", 11),
            relief="solid",
            bd=1,
            bg="white",
            fg="#1f2937",
            insertbackground="#1f2937",
            highlightbackground="#D1D5DB",
            highlightthickness=1
        )
        self.pnr_entry.grid(row=0, column=1, padx=(0, 20), pady=15)
        self.pnr_entry.bind("<Return>", lambda e: self.fetch_booking())

        _make_button(
            search_card,
            text="🔍  Find Booking",
            command=self.fetch_booking,
            bg="#2563EB"
        ).grid(row=0, column=2, padx=(0, 20), pady=15)

        # ---------------- Result Area ---------------- #

        self.result_holder = Frame(parent, bg="#F4F7FC")
        self.result_holder.pack(fill=BOTH, expand=True, padx=40, pady=(0, 30))

        self._show_placeholder()

    # ------------------------------------------------------------------ #

    def _clear_result_area(self):
        for widget in self.result_holder.winfo_children():
            widget.destroy()

    def _show_placeholder(self):
        self._clear_result_area()

        placeholder = Frame(
            self.result_holder,
            bg="white",
            highlightbackground="#D1D5DB",
            highlightthickness=1
        )
        placeholder.pack(fill=BOTH, expand=True)

        Label(
            placeholder,
            text="🎫",
            font=("Segoe UI", 40),
            bg="white",
            fg="#CBD5E1"
        ).pack(pady=(60, 10))

        Label(
            placeholder,
            text="No booking looked up yet",
            font=("Segoe UI", 12, "bold"),
            bg="white",
            fg="#94A3B8"
        ).pack()

        Label(
            placeholder,
            text="Enter a PNR above and click Find Booking",
            font=("Segoe UI", 10),
            bg="white",
            fg="#CBD5E1"
        ).pack(pady=(2, 60))

    # ------------------------------------------------------------------ #

    def _detail_block(self, parent, label, value, side=LEFT):
        block = Frame(parent, bg="white")
        block.pack(side=side, padx=(0, 50))

        Label(
            block,
            text=label,
            bg="white",
            fg="#94A3B8",
            font=("Segoe UI", 9, "bold")
        ).pack(anchor="w")

        Label(
            block,
            text=value,
            bg="white",
            fg="#1E293B",
            font=("Segoe UI", 13, "bold")
        ).pack(anchor="w")

    def _draw_result(self, data):

        pnr, name, flight_name, source, destination, seats, price, status = data

        self.current_pnr = pnr
        self.current_status = str(status).upper()

        self._clear_result_area()

        status_color = self.STATUS_COLORS.get(self.current_status, "#334155")

        card = Frame(
            self.result_holder,
            bg="white",
            highlightbackground="#D1D5DB",
            highlightthickness=1
        )
        card.pack(fill=X, pady=10)

        # -------- Header row -------- #

        header = Frame(card, bg="white")
        header.pack(fill=X, padx=30, pady=(25, 10))

        left = Frame(header, bg="white")
        left.pack(side=LEFT)

        Label(
            left,
            text="PASSENGER",
            bg="white",
            fg="#94A3B8",
            font=("Segoe UI", 9, "bold")
        ).pack(anchor="w")

        Label(
            left,
            text=name,
            bg="white",
            fg="#1E293B",
            font=("Segoe UI", 16, "bold")
        ).pack(anchor="w")

        right = Frame(header, bg="white")
        right.pack(side=RIGHT)

        Label(
            right,
            text="PNR",
            bg="white",
            fg="#94A3B8",
            font=("Segoe UI", 9, "bold")
        ).pack(anchor="e")

        Label(
            right,
            text=pnr,
            bg="white",
            fg="#1E293B",
            font=("Segoe UI", 16, "bold")
        ).pack(anchor="e")

        # -------- Route -------- #

        route = Frame(card, bg="white")
        route.pack(fill=X, padx=30, pady=10)

        Label(
            route,
            text=f"{source}  ✈  {destination}",
            bg="white",
            fg="#1E3A8A",
            font=("Segoe UI", 15, "bold")
        ).pack(side=LEFT)

        Label(
            route,
            text=flight_name,
            bg="white",
            fg="#64748B",
            font=("Segoe UI", 10)
        ).pack(side=RIGHT)

        # -------- Details -------- #

        details = Frame(card, bg="white")
        details.pack(fill=X, padx=30, pady=15)

        self._detail_block(details, "SEAT NO", str(seats))
        self._detail_block(details, "TICKET PRICE", f"₹{price:,.2f}")

        status_block = Frame(details, bg="white")
        status_block.pack(side=LEFT)

        Label(
            status_block,
            text="STATUS",
            bg="white",
            fg="#94A3B8",
            font=("Segoe UI", 9, "bold")
        ).pack(anchor="w")

        Label(
            status_block,
            text=self.current_status,
            bg="white",
            fg=status_color,
            font=("Segoe UI", 13, "bold")
        ).pack(anchor="w")

        # -------- Action row -------- #

        action_row = Frame(card, bg="#F8FAFC")
        action_row.pack(fill=X, pady=(15, 0))

        inner = Frame(action_row, bg="#F8FAFC")
        inner.pack(padx=30, pady=15, anchor="e")

        if self.current_status == "CANCELLED":

            Label(
                inner,
                text="This ticket is already cancelled.",
                bg="#F8FAFC",
                fg="#94A3B8",
                font=("Segoe UI", 10, "bold")
            ).pack(side=RIGHT)

        else:

            _make_button(
                inner,
                text="✖  Cancel This Ticket",
                command=self.cancel_booking,
                bg="#DC2626"
            ).pack(side=RIGHT)

    # ------------------------------------------------------------------ #

    def fetch_booking(self):

        pnr = self.pnr_entry.get().strip()

        if not pnr:
            messagebox.showerror("Error", "Please enter PNR")
            return

        try:

            conn = connect_db()
            cur = conn.cursor()

            query = """
            SELECT
                b.pnr,
                p.full_name,
                f.flight_name,
                f.source,
                f.destination,
                b.seats,
                b.total_price,
                b.status
            FROM bookings b
            JOIN passenger p
                ON b.passenger_id = p.passenger_id
            JOIN flights f
                ON b.flight_id = f.flight_id
            WHERE b.pnr = %s
            """

            cur.execute(query, (pnr,))
            row = cur.fetchone()

            conn.close()

            if row:
                self._draw_result(row)
            else:
                messagebox.showerror(
                    "PNR Not Found",
                    "No booking found for that PNR."
                )

        except Exception as e:
            messagebox.showerror("Error", str(e))

    def cancel_booking(self):

        if not self.current_pnr:
            return

        confirm = messagebox.askyesno(
            "Confirm Cancellation",
            f"Are you sure you want to cancel ticket {self.current_pnr}?\n"
            "This action cannot be undone."
        )

        if not confirm:
            return

        try:

            conn = connect_db()
            cur = conn.cursor()

            cur.execute("""
                UPDATE bookings
                SET status = 'CANCELLED'
                WHERE pnr = %s
            """, (self.current_pnr,))

            conn.commit()
            conn.close()

            messagebox.showinfo(
                "Ticket Cancelled",
                f"Ticket {self.current_pnr} has been cancelled."
            )

            self.fetch_booking()

        except Exception as e:
            messagebox.showerror("Error", str(e))