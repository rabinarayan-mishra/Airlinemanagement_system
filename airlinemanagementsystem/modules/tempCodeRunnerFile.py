import tkinter as tk
from tkinter import messagebox
import mysql.connector
import random
from modules.email_service import EmailService 


class BookFlight:

    def __init__(self, parent):

        self.parent = parent

        tk.Label(parent, text="BOOK FLIGHT",
                 font=("Arial", 18, "bold")).pack(pady=20)

        # ---------------- AADHAR ----------------
        tk.Label(parent, text="Aadhar Number").pack()
        self.aadhar = tk.Entry(parent)
        self.aadhar.pack()

        tk.Button(parent, text="Fetch User",
                  command=self.fetch_user,
                  bg="gray", fg="white").pack(pady=5)

        # ---------------- USER INFO ----------------
        tk.Label(parent, text="Name").pack()
        self.name_label = tk.Label(parent, text="")
        self.name_label.pack()

        tk.Label(parent, text="Email").pack()
        self.email_label = tk.Label(parent, text="")
        self.email_label.pack()

        tk.Label(parent, text="Gender").pack()
        self.gender_label = tk.Label(parent, text="")
        self.gender_label.pack()

        # ---------------- FROM ----------------
        tk.Label(parent, text="From").pack()
        self.source = tk.Entry(parent)
        self.source.pack()

        # ---------------- TO ----------------
        tk.Label(parent, text="To").pack()
        self.destination = tk.Entry(parent)
        self.destination.pack()

        # ---------------- FETCH FLIGHT ----------------
        tk.Button(parent, text="Fetch Flight",
                  command=self.fetch_flight,
                  bg="orange", fg="white").pack(pady=5)

        self.flight_info = tk.Label(parent, text="", fg="blue")
        self.flight_info.pack()

        # ---------------- BOOK BUTTON ----------------
        tk.Button(parent, text="BOOK FLIGHT",
                  command=self.book,
                  bg="blue", fg="white").pack(pady=10)

        self.passenger_id = None
        self.flight_id = None

    # ---------------- FETCH USER ----------------
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
                SELECT passenger_id, full_name, email, gender
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
            else:
                messagebox.showerror("Error", "Passenger not found")

        except Exception as e:
            messagebox.showerror("Error", str(e))

    # ---------------- FETCH FLIGHT ----------------
    def fetch_flight(self):

        src = self.source.get().strip()
        des = self.destination.get().strip()

        if not src or not des:
            messagebox.showerror("Error", "Enter From and To")
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
                SELECT flight_id, flight_name
                FROM flights
                WHERE source=%s AND destination=%s
            """, (src, des))

            flight = cur.fetchone()
            conn.close()

            if flight:
                self.flight_id = flight[0]
                self.flight_info.config(
                    text=f"Flight ID: {flight[0]} | Name: {flight[1]}"
                )
            else:
                messagebox.showerror("Error", "No Flight Found")

        except Exception as e:
            messagebox.showerror("Error", str(e))

    # ---------------- BOOK FLIGHT ----------------
    def book(self):

        if not self.passenger_id:
            messagebox.showerror("Error", "Fetch User First")
            return

        if not self.flight_id:
            messagebox.showerror("Error", "Fetch Flight First")
            return

        try:
            conn = mysql.connector.connect(
                host="localhost",
                user="root",
                password="rabi@2004",
                database="airline"
            )

            cur = conn.cursor()

            pnr = "PNR" + str(random.randint(10000, 99999))

            cur.execute("""
                INSERT INTO bookings
                (pnr, passenger_id, flight_id, status)
                VALUES (%s,%s,%s,%s)
            """, (
                pnr,
                self.passenger_id,
                self.flight_id,
                "CONFIRMED"
            ))

            conn.commit()
            conn.close()

            # ---------------- EMAIL ----------------
            email_service = EmailService()

            subject = "✈ Flight Booking Confirmation - " + pnr

            message = f"""
Dear {self.name_label.cget("text")},

Your flight booking is confirmed.

PNR: {pnr}
Flight ID: {self.flight_id}
Status: CONFIRMED

Thank you for choosing us ✈
"""

            to_email = self.email_label.cget("text")

            email_service.send_ticket_email(
                to_email=to_email,
                subject=subject,
                message_body=message
            )

            messagebox.showinfo("Success", f"Booking Confirmed!\nPNR: {pnr}")

        except Exception as e:
            messagebox.showerror("Error", str(e))