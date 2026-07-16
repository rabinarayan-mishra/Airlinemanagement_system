# from tkinter import *
# from tkinter import messagebox
# import mysql.connector


# class Login:
#     def __init__(self, root):
#         self.root = root
#         self.root.title("Login")
#         self.root.geometry("400x300")

#         Label(root, text="Email").pack()
#         self.email = Entry(root)
#         self.email.pack()

#         Label(root, text="Password").pack()
#         self.password = Entry(root, show="*")
#         self.password.pack()

#         Button(root, text="Login", command=self.login).pack()

#     def login(self):
#         email = self.email.get()
#         password = self.password.get()

#         if email == "" or password == "":
#             messagebox.showerror("Error", "All fields required")
#             return

#         try:
#             conn = mysql.connector.connect(
#                 host="localhost",
#                 user="root",
#                 password="YOUR_PASSWORD",
#                 database="airline"
#             )
#             cur = conn.cursor()

#             cur.execute(
#                 "SELECT passenger_id, full_name FROM passenger WHERE email=%s AND password=%s",
#                 (email, password)
#             )

#             user = cur.fetchone()

#             if user:
#                 messagebox.showinfo("Success", f"Welcome {user[1]}")
#                 self.root.destroy()
#                 BookingSystem(user[0])   # pass passenger_id
#             else:
#                 messagebox.showerror("Error", "Invalid login")

#             conn.close()

#         except Exception as e:
#             messagebox.showerror("DB Error", str(e))


# # ---------------- BOOKING SYSTEM ----------------

# class BookingSystem:
#     def __init__(self, passenger_id):
#         self.passenger_id = passenger_id

#         self.root = Tk()
#         self.root.title("Booking System")
#         self.root.geometry("500x400")

#         Label(self.root, text="Flight ID").pack()
#         self.flight_id = Entry(self.root)
#         self.flight_id.pack()

#         Label(self.root, text="Seats").pack()
#         self.seats = Entry(self.root)
#         self.seats.pack()

#         Button(self.root, text="Book Ticket", command=self.book).pack()

#         self.root.mainloop()

#     def book(self):
#         flight_id = self.flight_id.get()
#         seats = self.seats.get()

#         if flight_id == "" or seats == "":
#             messagebox.showerror("Error", "All fields required")
#             return

#         try:
#             conn = mysql.connector.connect(
#                 host="localhost",
#                 user="root",
#                 password="YOUR_PASSWORD",
#                 database="airline"
#             )
#             cur = conn.cursor()

#             # get flight price
#             cur.execute("SELECT price FROM flights WHERE flight_id=%s", (flight_id,))
#             flight = cur.fetchone()

#             if not flight:
#                 messagebox.showerror("Error", "Flight not found")
#                 return

#             price = flight[0]
#             total = price * int(seats)

#             # generate PNR safely
#             import random
#             pnr = "PNR" + str(random.randint(10000, 99999))

#             # insert booking
#             cur.execute("""
#                 INSERT INTO bookings (pnr, passenger_id, flight_id, seats, total_price)
#                 VALUES (%s, %s, %s, %s, %s)
#             """, (pnr, self.passenger_id, flight_id, seats, total))

#             conn.commit()
#             conn.close()

#             messagebox.showinfo("Success", f"Booking Confirmed!\nPNR: {pnr}")

#         except Exception as e:
#             messagebox.showerror("DB Error", str(e))


# # RUN
# if __name__ == "__main__":
#     root = Tk()
#     app = Login(root)
#     root.mainloop()