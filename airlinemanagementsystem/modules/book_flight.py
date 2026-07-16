import tkinter as tk
from tkinter import messagebox
import mysql.connector
import random

from modules.email_service import EmailService
from modules.whatsapp_service import WhatsAppService


class BookFlight:

    def __init__(self, parent):

        self.parent = parent
        parent.configure(bg="#F4F7FC")

        self.passenger_id = None
        self.flight_id = None
        self.phone = ""

        # ---------------- Title ---------------- #

        title_row = tk.Frame(parent, bg="#F4F7FC")
        title_row.pack(pady=(20, 5))

        tk.Label(
            title_row,
            text="✈",
            font=("Segoe UI", 40),
            bg="#F4F7FC",
            fg="#1E3A8A"
        ).pack(side=tk.LEFT, padx=(0, 12))

        tk.Label(
            title_row,
            text="BOOK FLIGHT",
            font=("Segoe UI", 24, "bold"),
            bg="#F4F7FC",
            fg="#1E3A8A"
        ).pack(side=tk.LEFT)

        tk.Label(
            parent,
            text="Search passenger and reserve a flight",
            font=("Segoe UI", 11),
            bg="#F4F7FC",
            fg="#64748B"
        ).pack()

        # ---------------- Card ---------------- #

        card = tk.Frame(
            parent,
            bg="white",
            highlightbackground="#D1D5DB",
            highlightthickness=1,
            bd=0
        )

        card.pack(pady=25, ipadx=30, ipady=20)

        # ---------------- Aadhar ---------------- #

        tk.Label(
            card,
            text="🪪 Aadhar Number",
            bg="white",
            fg="#334155",
            font=("Segoe UI", 11, "bold")
        ).grid(row=0, column=0, sticky="w", padx=20, pady=10)

        self.aadhar = tk.Entry(
            card,
            font=("Segoe UI", 11),
            width=35,
            relief="solid",
            bd=1,
            bg="white",
            fg="#1f2937",
            insertbackground="#1f2937",
            highlightbackground="#D1D5DB",
            highlightthickness=1
        )

        self.aadhar.grid(row=0, column=1, padx=20, pady=10)

        self._make_button(
            card,
            text="🔍  Fetch Passenger",
            command=self.fetch_user,
            bg="#2563EB",
            fg="white"
        ).grid(row=0, column=2, padx=15)

        # ---------------- Passenger Details ---------------- #

        tk.Label(
            card,
            text="👤 Passenger",
            bg="white",
            fg="#334155",
            font=("Segoe UI", 11, "bold")
        ).grid(row=1, column=0, sticky="w", padx=20, pady=10)

        self.name_label = tk.Label(
            card,
            text="Not Selected",
            bg="white",
            fg="#2563EB",
            font=("Segoe UI", 11)
        )

        self.name_label.grid(row=1, column=1, sticky="w")

        tk.Label(
            card,
            text="📧 Email",
            bg="white",
            fg="#334155",
            font=("Segoe UI", 11, "bold")
        ).grid(row=2, column=0, sticky="w", padx=20, pady=10)

        self.email_label = tk.Label(
            card,
            text="",
            bg="white",
            fg="#2563EB",
            font=("Segoe UI", 11)
        )

        self.email_label.grid(row=2, column=1, sticky="w")

        tk.Label(
            card,
            text="🚻 Gender",
            bg="white",
            fg="#334155",
            font=("Segoe UI", 11, "bold")
        ).grid(row=3, column=0, sticky="w", padx=20, pady=10)

        self.gender_label = tk.Label(
            card,
            text="",
            bg="white",
            fg="#2563EB",
            font=("Segoe UI", 11)
        )

        self.gender_label.grid(row=3, column=1, sticky="w")

        # ---------------- Source ---------------- #

        tk.Label(
            card,
            text="🛫 From",
            bg="white",
            fg="#334155",
            font=("Segoe UI", 11, "bold")
        ).grid(row=4, column=0, sticky="w", padx=20, pady=10)

        self.source = tk.Entry(
            card,
            font=("Segoe UI", 11),
            width=35,
            relief="solid",
            bd=1,
            bg="white",
            fg="#1f2937",
            insertbackground="#1f2937",
            highlightbackground="#D1D5DB",
            highlightthickness=1
        )

        self.source.grid(row=4, column=1, padx=20, pady=10)

        # ---------------- Destination ---------------- #

        tk.Label(
            card,
            text="🛬 To",
            bg="white",
            fg="#334155",
            font=("Segoe UI", 11, "bold")
        ).grid(row=5, column=0, sticky="w", padx=20, pady=10)

        self.destination = tk.Entry(
            card,
            font=("Segoe UI", 11),
            width=35,
            relief="solid",
            bd=1,
            bg="white",
            fg="#1f2937",
            insertbackground="#1f2937",
            highlightbackground="#D1D5DB",
            highlightthickness=1
        )

        self.destination.grid(row=5, column=1, padx=20, pady=10)

        self._make_button(
            card,
            text="✈  Fetch Flight",
            command=self.fetch_flight,
            bg="#F59E0B",
            fg="white"
        ).grid(row=5, column=2, padx=15)

        # ---------------- Flight Info ---------------- #

        tk.Label(
            card,
            text="Flight Information",
            bg="white",
            fg="#334155",
            font=("Segoe UI", 11, "bold")
        ).grid(row=6, column=0, sticky="w", padx=20, pady=15)

        self.flight_info = tk.Label(
            card,
            text="No Flight Selected",
            bg="white",
            fg="#2563EB",
            font=("Segoe UI", 11, "bold")
        )

        self.flight_info.grid(row=6, column=1, sticky="w")

        # ---------------- Book Button ---------------- #

        self._make_button(
            parent,
            text="🛫  BOOK FLIGHT",
            command=self.book,
            bg="#16A34A",
            fg="white",
            font=("Segoe UI", 12, "bold"),
            padx=25,
            pady=10
        ).pack(pady=20)

    # ------------------------------------------------------------------ #
    # Custom "button" built from a Label.
    #
    # On macOS, native Tk/Aqua buttons ignore the `bg` option and render
    # with the system's default (white/gray) button chrome, which is why
    # colored buttons were showing up blank/clipped. Using a styled Label
    # bound to mouse clicks guarantees the colors render identically on
    # macOS, Windows, and Linux.
    # ------------------------------------------------------------------ #
    def _make_button(self, parent, text, command, bg, fg="white",
                      font=("Segoe UI", 10, "bold"), padx=15, pady=8):

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

    def fetch_user(self):

        aadhar = self.aadhar.get().strip()

        if not aadhar:
            messagebox.showerror("Error", "Enter Aadhar")
            return

        try:

            conn = mysql.connector.connect(
                host="localhost",
                user="root",
                password="rabi@2004",
                database="airline"
            )

            cur = conn.cursor()

            cur.execute("""
                SELECT passenger_id,
                       full_name,
                       email,
                       gender,
                       phone
                FROM passenger
                WHERE aadhar=%s
            """, (aadhar,))

            data = cur.fetchone()

            conn.close()

            if data:

                self.passenger_id = data[0]

                self.name_label.config(text=data[1])
                self.email_label.config(text=data[2])
                self.gender_label.config(text=data[3])

                self.phone = data[4]

            else:
                messagebox.showerror(
                    "Error",
                    "Passenger not found"
                )

        except Exception as e:
            messagebox.showerror("Error", str(e))

    def fetch_flight(self):

        src = self.source.get().strip()
        des = self.destination.get().strip()

        if not src or not des:
            messagebox.showerror(
                "Error",
                "Enter From and To"
            )
            return

        try:

            conn = mysql.connector.connect(
                host="localhost",
                user="root",
                password="rabi@2004",
                database="airline"
            )

            cur = conn.cursor()

            cur.execute("""
                SELECT flight_id,
                       flight_name
                FROM flights
                WHERE source=%s
                AND destination=%s
            """, (src, des))

            flight = cur.fetchone()

            conn.close()

            if flight:

                self.flight_id = flight[0]

                self.flight_info.config(
                    text=f"Flight ID: {flight[0]} | {flight[1]}"
                )

            else:
                messagebox.showerror(
                    "Error",
                    "No Flight Found"
                )

        except Exception as e:
            messagebox.showerror("Error", str(e))

    def book(self):

        if not self.passenger_id:
            messagebox.showerror(
                "Error",
                "Fetch User First"
            )
            return

        if not self.flight_id:
            messagebox.showerror(
                "Error",
                "Fetch Flight First"
            )
            return

        try:

            conn = mysql.connector.connect(
                host="localhost",
                user="root",
                password="rabi@2004",
                database="airline"
            )

            cur = conn.cursor()

            cur.execute("""
                SELECT COUNT(*)
                FROM bookings
                WHERE flight_id=%s
                AND status='CONFIRMED'
            """, (self.flight_id,))

            booked_seats = cur.fetchone()[0]

            if booked_seats >= 30:

                messagebox.showerror(
                    "Error",
                    "No Seats Available"
                )

                conn.close()
                return

            seat_no = booked_seats + 1

            pnr = "PNR" + str(
                random.randint(10000, 99999)
            )

            total_price = 9000.00

            cur.execute("""
                INSERT INTO bookings
                (pnr, passenger_id, flight_id,
                 seats, total_price, status)
                VALUES (%s,%s,%s,%s,%s,%s)
            """, (
                pnr,
                self.passenger_id,
                self.flight_id,
                seat_no,
                total_price,
                "CONFIRMED"
            ))

            conn.commit()
            conn.close()

            subject = f"Flight Booking Confirmation - {pnr}"

            message = f"""
AIRLINE MANAGEMENT SYSTEM

BOOKING CONFIRMED

Passenger : {self.name_label.cget('text')}
PNR       : {pnr}
Flight ID : {self.flight_id}
Seat No   : {seat_no}
Price     : ₹{total_price}
Status    : CONFIRMED
"""

            EmailService().send_ticket_email(
                to_email=self.email_label.cget("text"),
                subject=subject,
                message_body=message
            )

            if self.phone:
                WhatsAppService.send_message(
                    self.phone,
                    message
                )

            messagebox.showinfo(
                "Success",
                f"Booking Confirmed!\nPNR: {pnr}\nSeat No: {seat_no}"
            )

        except Exception as e:
            messagebox.showerror(
                "Error",
                str(e)
            )