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


class BoardingPass:

    STATUS_COLORS = {
        "CONFIRMED": ("#DCFCE7", "#16A34A"),
        "CANCELLED": ("#FEE2E2", "#DC2626"),
    }

    def __init__(self, parent):

        self.parent = parent
        parent.configure(bg="#F4F7FC")

        # ---------------- Title ---------------- #

        title_row = Frame(parent, bg="#F4F7FC")
        title_row.pack(pady=(20, 5))

        Label(
            title_row,
            text="🎫",
            font=("Segoe UI", 40),
            bg="#F4F7FC",
            fg="#1E3A8A"
        ).pack(side=LEFT, padx=(0, 12))

        Label(
            title_row,
            text="BOARDING PASS",
            font=("Segoe UI", 24, "bold"),
            bg="#F4F7FC",
            fg="#1E3A8A"
        ).pack(side=LEFT)

        Label(
            parent,
            text="Enter a PNR to generate the digital boarding pass",
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
        self.pnr_entry.bind("<Return>", lambda e: self.generate())

        _make_button(
            search_card,
            text="✈  Generate Boarding Pass",
            command=self.generate,
            bg="#2563EB"
        ).grid(row=0, column=2, padx=(0, 20), pady=15)

        # ---------------- Ticket Area ---------------- #

        self.ticket_holder = Frame(parent, bg="#F4F7FC")
        self.ticket_holder.pack(fill=BOTH, expand=True, padx=40, pady=(0, 30))

        self._show_placeholder()

    # ------------------------------------------------------------------ #

    def _clear_ticket_area(self):
        for widget in self.ticket_holder.winfo_children():
            widget.destroy()

    def _show_placeholder(self):
        self._clear_ticket_area()

        placeholder = Frame(
            self.ticket_holder,
            bg="white",
            highlightbackground="#D1D5DB",
            highlightthickness=1
        )
        placeholder.pack(fill=BOTH, expand=True)

        Label(
            placeholder,
            text="🛫",
            font=("Segoe UI", 40),
            bg="white",
            fg="#CBD5E1"
        ).pack(pady=(60, 10))

        Label(
            placeholder,
            text="No boarding pass generated yet",
            font=("Segoe UI", 12, "bold"),
            bg="white",
            fg="#94A3B8"
        ).pack()

        Label(
            placeholder,
            text="Enter a valid PNR above to see the ticket here",
            font=("Segoe UI", 10),
            bg="white",
            fg="#CBD5E1"
        ).pack(pady=(2, 60))

    # ------------------------------------------------------------------ #

    def _draw_ticket(self, data):

        pnr, name, flight_name, source, destination, seats, price, status = data

        self._clear_ticket_area()

        badge_bg, badge_fg = self.STATUS_COLORS.get(
            str(status).upper(), ("#F1F5F9", "#334155")
        )

        outer = Frame(
            self.ticket_holder,
            bg="white",
            highlightbackground="#D1D5DB",
            highlightthickness=1
        )
        outer.pack(fill=X, pady=10)

        # -------- Top strip -------- #

        top = Frame(outer, bg="#1E3A8A")
        top.pack(fill=X)

        Label(
            top,
            text="✈  AIRLINE SYSTEM",
            bg="#1E3A8A",
            fg="white",
            font=("Segoe UI", 12, "bold")
        ).pack(side=LEFT, padx=20, pady=12)

        status_badge = Label(
            top,
            text=f"  {status}  ",
            bg=badge_fg,
            fg="white",
            font=("Segoe UI", 9, "bold")
        )
        status_badge.pack(side=RIGHT, padx=20, pady=12)

        # -------- Passenger + PNR row -------- #

        info_row = Frame(outer, bg="white")
        info_row.pack(fill=X, padx=30, pady=(20, 10))

        left_info = Frame(info_row, bg="white")
        left_info.pack(side=LEFT)

        Label(
            left_info,
            text="PASSENGER",
            bg="white",
            fg="#94A3B8",
            font=("Segoe UI", 9, "bold")
        ).pack(anchor="w")

        Label(
            left_info,
            text=name,
            bg="white",
            fg="#1E293B",
            font=("Segoe UI", 16, "bold")
        ).pack(anchor="w")

        right_info = Frame(info_row, bg="white")
        right_info.pack(side=RIGHT)

        Label(
            right_info,
            text="PNR",
            bg="white",
            fg="#94A3B8",
            font=("Segoe UI", 9, "bold")
        ).pack(anchor="e")

        Label(
            right_info,
            text=pnr,
            bg="white",
            fg="#1E293B",
            font=("Segoe UI", 16, "bold")
        ).pack(anchor="e")

        # -------- Route row -------- #

        route_row = Frame(outer, bg="white")
        route_row.pack(fill=X, padx=30, pady=20)

        from_box = Frame(route_row, bg="white")
        from_box.pack(side=LEFT)

        Label(
            from_box,
            text=source,
            bg="white",
            fg="#1E3A8A",
            font=("Segoe UI", 22, "bold")
        ).pack(anchor="w")

        Label(
            from_box,
            text="FROM",
            bg="white",
            fg="#94A3B8",
            font=("Segoe UI", 9, "bold")
        ).pack(anchor="w")

        Label(
            route_row,
            text=f"✈  {flight_name}  ✈",
            bg="white",
            fg="#64748B",
            font=("Segoe UI", 11, "bold")
        ).pack(side=LEFT, expand=True)

        to_box = Frame(route_row, bg="white")
        to_box.pack(side=RIGHT)

        Label(
            to_box,
            text=destination,
            bg="white",
            fg="#1E3A8A",
            font=("Segoe UI", 22, "bold")
        ).pack(anchor="e")

        Label(
            to_box,
            text="TO",
            bg="white",
            fg="#94A3B8",
            font=("Segoe UI", 9, "bold")
        ).pack(anchor="e")

        # -------- Dashed separator -------- #

        sep = Canvas(outer, height=2, bg="white", highlightthickness=0)
        sep.pack(fill=X, padx=30)
        sep.bind(
            "<Configure>",
            lambda e: self._draw_dashes(sep, e.width)
        )

        # -------- Seat / Price / Details row -------- #

        details_row = Frame(outer, bg="white")
        details_row.pack(fill=X, padx=30, pady=20)

        self._detail_block(details_row, "SEAT NO", str(seats), side=LEFT)
        self._detail_block(details_row, "TICKET PRICE", f"₹{price:,.2f}", side=LEFT)
        self._detail_block(details_row, "CLASS", "ECONOMY", side=LEFT)

        # -------- Barcode strip -------- #

        barcode_holder = Frame(outer, bg="#F8FAFC")
        barcode_holder.pack(fill=X)

        barcode = Canvas(
            barcode_holder,
            height=50,
            bg="#F8FAFC",
            highlightthickness=0
        )
        barcode.pack(fill=X, padx=30, pady=10)
        barcode.bind(
            "<Configure>",
            lambda e: self._draw_barcode(barcode, e.width, pnr)
        )

        Label(
            outer,
            text="HAVE A SAFE JOURNEY",
            bg="white",
            fg="#94A3B8",
            font=("Segoe UI", 9, "bold")
        ).pack(pady=(0, 15))

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

    @staticmethod
    def _draw_dashes(canvas, width):
        canvas.delete("all")
        x = 0
        while x < width:
            canvas.create_line(x, 1, x + 8, 1, fill="#CBD5E1", width=2)
            x += 14

    @staticmethod
    def _draw_barcode(canvas, width, seed_text):
        canvas.delete("all")
        seed = sum(ord(c) for c in seed_text) or 1
        x = 0
        i = 0
        while x < width - 4:
            bar_w = 2 if (seed * (i + 1)) % 3 else 4
            canvas.create_rectangle(
                x, 5, x + bar_w, 40,
                fill="#334155", width=0
            )
            x += bar_w + 3
            i += 1

    # ------------------------------------------------------------------ #

    def generate(self):

        try:

            conn = connect_db()
            cur = conn.cursor()

            pnr = self.pnr_entry.get().strip()

            if not pnr:
                messagebox.showerror(
                    "Error",
                    "Please enter PNR"
                )
                return

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
                self._draw_ticket(row)
            else:
                messagebox.showerror(
                    "PNR Not Found",
                    "No booking found.\nCheck the PNR from Book Flight."
                )

        except Exception as e:

            messagebox.showerror(
                "Error",
                str(e)
            )