from tkinter import *
from tkinter import messagebox


# Demo Users
users = {
    "admin": {
        "password": "admin123",
        "role": "admin"
    },
    "user": {
        "password": "user123",
        "role": "user"
    }
}


def login_system(open_dashboard):

    login = Tk()
    login.title("Airline Management System")
    login.geometry("450x350")
    login.resizable(False, False)

    # Heading
    Label(
        login,
        text="✈ AIRLINE MANAGEMENT SYSTEM",
        font=("Arial", 16, "bold"),
        fg="blue"
    ).pack(pady=20)

    # Username
    Label(
        login,
        text="Username",
        font=("Arial", 12)
    ).pack(pady=5)

    username_entry = Entry(
        login,
        width=30,
        font=("Arial", 12)
    )
    username_entry.pack()

    # Password
    Label(
        login,
        text="Password",
        font=("Arial", 12)
    ).pack(pady=10)

    password_entry = Entry(
        login,
        width=30,
        show="*",
        font=("Arial", 12)
    )
    password_entry.pack()

    def check_login():

        username = username_entry.get().strip()
        password = password_entry.get().strip()

        if username in users:

            if users[username]["password"] == password:

                role = users[username]["role"]

                messagebox.showinfo(
                    "Success",
                    f"Welcome {username}"
                )

                login.destroy()

                open_dashboard(role)

            else:
                messagebox.showerror(
                    "Login Failed",
                    "Incorrect Password"
                )

        else:
            messagebox.showerror(
                "Login Failed",
                "User Not Found"
            )

    Button(
        login,
        text="LOGIN",
        width=15,
        bg="green",
        fg="black",
        font=("Arial", 12, "bold"),
        command=check_login
    ).pack(pady=25)

    login.mainloop()


# Test Auth
if __name__ == "__main__":

    def test(role):
        print("Logged in as:", role)

    login_system(test)