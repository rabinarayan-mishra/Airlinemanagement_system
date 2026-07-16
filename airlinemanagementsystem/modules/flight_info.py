from tkinter import *
from tkinter import ttk
from db import connect_db


def _make_button(parent, text, command, bg, fg="white",
                  font=("Segoe UI", 10, "bold"), padx=15, pady=6):
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


def flight_info_gui(parent):

    parent.configure(bg="#F4F7FC")

    # ---------------- Title ---------------- #

    title_row = Frame(parent, bg="#F4F7FC")
    title_row.pack(pady=(20, 5))

    Label(
        title_row,
        text="🛩",
        font=("Segoe UI", 40),
        bg="#F4F7FC",
        fg="#1E3A8A"
    ).pack(side=LEFT, padx=(0, 12))

    Label(
        title_row,
        text="FLIGHT INFORMATION",
        font=("Segoe UI", 24, "bold"),
        bg="#F4F7FC",
        fg="#1E3A8A"
    ).pack(side=LEFT)

    Label(
        parent,
        text="All flights currently available in the system",
        font=("Segoe UI", 11),
        bg="#F4F7FC",
        fg="#64748B"
    ).pack()

    # ---------------- Toolbar ---------------- #

    toolbar = Frame(parent, bg="#F4F7FC")
    toolbar.pack(fill=X, padx=40, pady=(15, 5))

    count_label = Label(
        toolbar,
        text="",
        font=("Segoe UI", 10, "bold"),
        bg="#F4F7FC",
        fg="#334155"
    )
    count_label.pack(side=LEFT)

    # ---------------- Card ---------------- #

    card = Frame(
        parent,
        bg="white",
        highlightbackground="#D1D5DB",
        highlightthickness=1,
        bd=0
    )

    card.pack(fill=BOTH, expand=True, padx=40, pady=(5, 30))

    table_frame = Frame(card, bg="white")
    table_frame.pack(fill=BOTH, expand=True, padx=15, pady=15)

    # ---------------- Treeview Style ---------------- #

    style = ttk.Style()
    style.theme_use("clam")

    style.configure(
        "Flights.Treeview",
        font=("Segoe UI", 10),
        rowheight=34,
        background="white",
        fieldbackground="white",
        foreground="#1f2937",
        borderwidth=0
    )

    style.configure(
        "Flights.Treeview.Heading",
        font=("Segoe UI", 10, "bold"),
        background="#1E3A8A",
        foreground="white",
        relief="flat",
        padding=8
    )

    style.map(
        "Flights.Treeview.Heading",
        background=[("active", "#1E40AF")]
    )

    style.map(
        "Flights.Treeview",
        background=[("selected", "#DBEAFE")],
        foreground=[("selected", "#1E3A8A")]
    )

    style.configure(
        "Flights.Vertical.TScrollbar",
        background="#CBD5E1",
        troughcolor="white",
        bordercolor="white",
        arrowcolor="#334155",
        relief="flat"
    )

    columns = (
        "ID",
        "Flight Name",
        "Source",
        "Destination",
        "Departure",
        "Arrival",
        "Price",
        "Seats"
    )

    col_widths = {
        "ID": 60,
        "Flight Name": 150,
        "Source": 110,
        "Destination": 110,
        "Departure": 140,
        "Arrival": 140,
        "Price": 100,
        "Seats": 90
    }

    tree = ttk.Treeview(
        table_frame,
        columns=columns,
        show="headings",
        height=18,
        style="Flights.Treeview"
    )

    for col in columns:
        tree.heading(col, text=col)
        tree.column(
            col,
            width=col_widths.get(col, 120),
            anchor="center"
        )

    # Alternating row colors + low-seat warning
    tree.tag_configure("evenrow", background="#F8FAFC")
    tree.tag_configure("oddrow", background="white")
    tree.tag_configure("lowseats", foreground="#DC2626")
    tree.tag_configure("goodseats", foreground="#16A34A")

    scrollbar = ttk.Scrollbar(
        table_frame,
        orient="vertical",
        command=tree.yview,
        style="Flights.Vertical.TScrollbar"
    )

    tree.configure(yscrollcommand=scrollbar.set)

    tree.pack(side=LEFT, fill=BOTH, expand=True)
    scrollbar.pack(side=RIGHT, fill=Y)

    # ---------------- Data Loading ---------------- #

    def load_data():

        for row in tree.get_children():
            tree.delete(row)

        try:
            conn = connect_db()
            cur = conn.cursor(buffered=True)

            cur.execute("""
                SELECT flight_id,
                       flight_name,
                       source,
                       destination,
                       departure_time,
                       arrival_time,
                       price,
                       seats_available
                FROM flights
                ORDER BY flight_id
            """)

            rows = cur.fetchall()

            conn.close()

            for i, row in enumerate(rows):

                row = list(row)
                row[6] = f"₹{row[6]:,.2f}"

                stripe_tag = "evenrow" if i % 2 == 0 else "oddrow"
                seats_left = row[7]
                seat_tag = "lowseats" if seats_left is not None and seats_left <= 5 else "goodseats"

                tree.insert(
                    "",
                    END,
                    values=row,
                    tags=(stripe_tag, seat_tag)
                )

            count_label.config(
                text=f"{len(rows)} flight(s) found",
                fg="#334155"
            )

        except Exception as e:
            count_label.config(
                text=f"Database Error: {e}",
                fg="#DC2626"
            )

    _make_button(
        toolbar,
        text="🔄  Refresh",
        command=load_data,
        bg="#2563EB"
    ).pack(side=RIGHT)

    load_data()


# For testing separately
if __name__ == "__main__":
    root = Tk()
    root.title("Flight Information")
    root.geometry("1100x700")

    flight_info_gui(root)

    root.mainloop()