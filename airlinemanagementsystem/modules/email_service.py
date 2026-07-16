import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart


class EmailService:

    def __init__(self):
        self.smtp_server = "smtp.gmail.com"
        self.smtp_port = 587

        self.email = "mrabinarayan43@gmail.com"
        self.password = "vrnhgpmpmulookwo"

    def send_ticket_email(self, to_email, subject, message_body):

        try:
            msg = MIMEMultipart()
            msg["From"] = self.email
            msg["To"] = to_email
            msg["Subject"] = subject

            msg.attach(MIMEText(message_body, "plain"))

            server = smtplib.SMTP(self.smtp_server, self.smtp_port)
            server.starttls()
            server.login(self.email, self.password)

            server.send_message(msg)
            server.quit()

            print("EMAIL SENT SUCCESSFULLY")
            return True

        except Exception as e:
            if "Duplicate entry" in str(e):
                messagebox.showerror(
            "Duplicate Email",
            "This email is already registered."
        )
            else:
                messagebox.showerror("Database Error", str(e))