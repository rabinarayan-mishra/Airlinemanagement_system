import tkinter as tk
from tkinter import ttk, messagebox
from db import connect_db


class AddCustomer:

    def __init__(self, parent):

        self.parent = parent
        parent.configure(bg="#F4F7FC")

        # ---------------- Title ---------------- #
        title = tk.Label(
            parent,
            text="✈ ADD PASSENGER",
            font=("Segoe UI", 24, "bold"),
            bg="#F4F7FC",
            fg="#1E3A8A"
        )
        title.pack(pady=(25, 10))

        subtitle = tk.Label(
            parent,
            text="Enter passenger information",
            font=("Segoe UI", 11),
            bg="#F4F7FC",
            fg="#64748B"
        )
        subtitle.pack()

        # ---------------- Card ---------------- #
        card = tk.Frame(
            parent,
            bg="white",
            highlightbackground="#D1D5DB",
            highlightthickness=1,
            bd=0
        )
        card.pack(pady=25, ipadx=30, ipady=25)

        # ---------------- Variables ---------------- #

        self.full_name = tk.StringVar()
        self.gender = tk.StringVar()
        self.phone = tk.StringVar()
        self.email = tk.StringVar()
        self.nationality = tk.StringVar()
        self.aadhar = tk.StringVar()
        self.passport = tk.StringVar()

        # ---------------- Style ---------------- #

        style = ttk.Style()
        style.theme_use("clam")

        style.configure(
            "Modern.TEntry",
            fieldbackground="#F8FAFC",
            bordercolor="#CBD5E1",
            lightcolor="#CBD5E1",
            darkcolor="#CBD5E1",
            padding=8,
            font=("Segoe UI", 11)
        )

        style.configure(
            "Modern.TCombobox",
            padding=8,
            font=("Segoe UI", 11)
        )

        # ---------------- Fields ---------------- #

        fields = [
            ("👤 Full Name", self.full_name),
            ("📱 Phone", self.phone),
            ("📧 Email", self.email),
            ("🌍 Nationality", self.nationality),
            ("🪪 Aadhar", self.aadhar),
            ("🛂 Passport", self.passport),
        ]

        for i, (label, var) in enumerate(fields):

            tk.Label(
                card,
                text=label,
                bg="white",
                fg="#334155",
                font=("Segoe UI", 11, "bold")
            ).grid(row=i, column=0, sticky="w", padx=20, pady=12)

            ttk.Entry(
                card,
                textvariable=var,
                width=35,
                style="Modern.TEntry"
            ).grid(row=i, column=1, padx=20, pady=12)

        # ---------------- Gender ---------------- #

        tk.Label(
            card,
            text="🚻 Gender",
            bg="white",
            fg="#334155",
            font=("Segoe UI", 11, "bold")
        ).grid(row=6, column=0, sticky="w", padx=20, pady=12)

        gender = ttk.Combobox(
            card,
            textvariable=self.gender,
            values=["Male", "Female", "Other"],
            state="readonly",
            width=33,
            style="Modern.TCombobox"
        )

        gender.grid(row=6, column=1, padx=20, pady=12)
        gender.current(0)

        # ---------------- Save Button ---------------- #

        self.save_btn = tk.Button(
            parent,
            text="💾 SAVE PASSENGER",
            font=("Segoe UI", 11, "bold"),
            bg="#2563EB",
            fg="white",
            activebackground="#1D4ED8",
            activeforeground="white",
            relief="flat",
            bd=0,
            padx=20,
            pady=10,
            cursor="hand2",
            command=self.save
        )

        self.save_btn.pack(pady=20)

        # Hover Effect

        self.save_btn.bind("<Enter>", self.on_enter)
        self.save_btn.bind("<Leave>", self.on_leave)

    # ---------------- Button Hover ---------------- #

    def on_enter(self, event):
        self.save_btn.config(bg="#1D4ED8")

    def on_leave(self, event):
        self.save_btn.config(bg="#2563EB")

    # ---------------- Save Function ---------------- #

    def save(self):

        if self.full_name.get().strip() == "":
            messagebox.showerror("Error", "Full Name is required")
            return

        if self.email.get().strip() == "":
            messagebox.showerror("Error", "Email is required")
            return

        try:
            conn = connect_db()
            cur = conn.cursor()

            cur.execute("""
                INSERT INTO passenger
                (full_name, gender, phone, email, nationality, aadhar, passport)
                VALUES (%s,%s,%s,%s,%s,%s,%s)
            """, (
                self.full_name.get(),
                self.gender.get(),
                self.phone.get(),
                self.email.get(),
                self.nationality.get(),
                self.aadhar.get(),
                self.passport.get()
            ))

            conn.commit()
            conn.close()

            messagebox.showinfo(
                "Success",
                "Passenger Added Successfully"
            )

            self.full_name.set("")
            self.gender.set("Male")
            self.phone.set("")
            self.email.set("")
            self.nationality.set("")
            self.aadhar.set("")
            self.passport.set("")

        except Exception as e:
            messagebox.showerror(
                "Database Error",
                str(e)
            )