from tkinter import *
from auth import login_system

from modules.add_customer import AddCustomer
from modules.book_flight import BookFlight
from modules.journey_details import JourneyDetails
from modules.flight_info import flight_info_gui
from modules.boarding_pass import BoardingPass
from modules.cancel_ticket import CancelTicket


# ================= COLORS =================
BG_COLOR = "white"
SIDEBAR_COLOR = "#1f2937"
TEXT_COLOR = "#1f2937"
BUTTON_COLOR = "#2563eb"
BUTTON_TEXT = "black"

TITLE_FONT = ("Segoe UI", 22, "bold")
HEADER_FONT = ("Segoe UI", 26, "bold")
BUTTON_FONT = ("Segoe UI", 11, "bold")


def dashboard(role):

    root = Tk()
    root.title("Airline Management System")
    root.geometry("1200x700")
    root.configure(bg=BG_COLOR)

    # ================= SIDEBAR =================
    sidebar = Frame(root, bg=SIDEBAR_COLOR, width=250)
    sidebar.pack(side=LEFT, fill=Y)
    sidebar.pack_propagate(False)

    # ================= MAIN AREA =================
    main_frame = Frame(root, bg=BG_COLOR)
    main_frame.pack(side=RIGHT, expand=True, fill=BOTH)

    def clear():
        for widget in main_frame.winfo_children():
            widget.destroy()

    def open_module(module):
        clear()
        module(main_frame)

    # ================= LOGO =================
    Label(
        sidebar,
        text="✈ AIRLINE\nSYSTEM",
        bg=SIDEBAR_COLOR,
        fg="white",
        font=TITLE_FONT,
        justify=CENTER
    ).pack(pady=30)

    # ================= MODULE FUNCTIONS =================
    def open_add():
        clear()
        AddCustomer(main_frame)

    def open_book():
        clear()
        BookFlight(main_frame)

    def open_journey():
        clear()
        JourneyDetails(main_frame)

    # ================= BUTTON STYLE =================
    btn_style = {
        "width": 20,
        "bg": BUTTON_COLOR,
        "fg": BUTTON_TEXT,
        "font": BUTTON_FONT,
        "relief": FLAT,
        "cursor": "hand2",
        "activebackground": "#1d4ed8",
        "activeforeground": "white"
    }

    Button(
        sidebar,
        text="Add Customer",
        command=open_add,
        **btn_style
    ).pack(pady=8)

    Button(
        sidebar,
        text="Book Flight",
        command=open_book,
        **btn_style
    ).pack(pady=8)

    Button(
        sidebar,
        text="Journey Details",
        command=open_journey,
        **btn_style
    ).pack(pady=8)

    Button(
        sidebar,
        text="Flight Info",
        command=lambda: open_module(flight_info_gui),
        **btn_style
    ).pack(pady=8)

    Button(
        sidebar,
        text="Boarding Pass",
        command=lambda: open_module(BoardingPass),
        **btn_style
    ).pack(pady=8)

    Button(
        sidebar,
        text="Cancel Ticket",
        command=lambda: open_module(CancelTicket),
        **btn_style
    ).pack(pady=8)

    # ================= DASHBOARD =================
    Label(
        main_frame,
        text=f"{role.upper()} DASHBOARD",
        bg=BG_COLOR,
        fg=TEXT_COLOR,
        font=HEADER_FONT
    ).pack(pady=40)

    Label(
        main_frame,
        text="Welcome to Airline Management System",
        bg=BG_COLOR,
        fg="#6b7280",
        font=("Segoe UI", 14)
    ).pack()

    Label(
        main_frame,
        text="Select an option from the left menu.",
        bg=BG_COLOR,
        fg="#9ca3af",
        font=("Segoe UI", 11)
    ).pack(pady=10)

    root.mainloop()


if __name__ == "__main__":
    login_system(dashboard)