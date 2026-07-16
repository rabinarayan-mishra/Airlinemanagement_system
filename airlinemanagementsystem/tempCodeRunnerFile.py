from tkinter import *
from auth import login_system

# Modules
from modules.add_customer import AddCustomer
from modules.book_flight import BookFlight
from modules.flight_info import flight_info_gui
from modules.journey_details import JourneyDetails
from modules.boarding_pass import BoardingPass
from modules.cancel_ticket import CancelTicket


def dashboard(role):

    root = Tk()
    root.title("Airline Management System")
    root.geometry("1200x700")
    root.configure(bg="white")

    # ---------------- SIDEBAR ---------------- #
    sidebar = Frame(root, bg="#1f2937", width=250)
    sidebar.pack(side=LEFT, fill=Y)

    # ---------------- MAIN AREA ---------------- #
    main_frame = Frame(root, bg="white")
    main_frame.pack(side=RIGHT, expand=True, fill=BOTH)

    def clear_main():
        for widget in main_frame.winfo_children():
            widget.destroy()

    # ---------------- HEADER ---------------- #
    Label(
        sidebar,
        text="✈ AIRLINE",
        bg="#1f2937",
        fg="white",
        font=("Arial", 20, "bold")
    ).pack(pady=20)

    # ---------------- FUNCTIONS ---------------- #

    def open_add_customer():
        clear_main()
        AddCustomer(main_frame)

    def open_book_flight():
        clear_main()
        BookFlight(main_frame)

    def open_flight_info():
        clear_main()
        flight_info_gui(main_frame)

    def open_journey():
        clear_main()
        JourneyDetails(main_frame)

    def open_boarding():
        clear_main()
        BoardingPass(main_frame)

    def open_cancel():
        clear_main()
        CancelTicket(main_frame)

    # ---------------- BUTTONS ---------------- #

    Button(
        sidebar,
        text="Add Customer",
        width=20,
        command=open_add_customer
    ).pack(pady=10)

    Button(
        sidebar,
        text="Book Flight",
        width=20,
        command=open_book_flight
    ).pack(pady=10)

    Button(
        sidebar,
        text="Flight Info",
        width=20,
        command=open_flight_info
    ).pack(pady=10)

    Button(
        sidebar,
        text="Journey Details",
        width=20,
        command=open_journey
    ).pack(pady=10)

    Button(
        sidebar,
        text="Boarding Pass",
        width=20,
        command=open_boarding
    ).pack(pady=10)

    Button(
        sidebar,
        text="Cancel Ticket",
        width=20,
        command=open_cancel
    ).pack(pady=10)

    # ---------------- DASHBOARD HOME ---------------- #

    Label(
        main_frame,
        text=f"{role.upper()} DASHBOARD",
        bg="white",
        fg="black",
        font=("Arial", 24, "bold")
    ).pack(pady=40)

    Label(
        main_frame,
        text="Welcome to Airline Management System",
        bg="white",
        fg="gray",
        font=("Arial", 14)
    ).pack()

    root.mainloop()


# ---------------- START APP ---------------- #

if __name__ == "__main__":
    login_system(dashboard)