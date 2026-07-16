from tkinter import *
from db import connect_db

def flight_info_gui(parent):

    frame = Frame(parent, bg="white")
    frame.pack(fill=BOTH, expand=True)

    Label(frame, text="✈ AVAILABLE FLIGHTS",
          font=("Arial", 18, "bold")).pack(pady=10)

    text = Text(frame, width=100, height=25)
    text.pack()

    conn = connect_db()
    cur = conn.cursor()
    cur.execute("SELECT * FROM flights")
    data = cur.fetchall()

    for row in data:
        text.insert(END, str(row) + "\n\n")

    conn.close()