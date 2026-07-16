print("🔥 FILE IS RUNNING")

from modules.email_service import EmailService

print("📧 Import successful")

email_service = EmailService()

print("📦 EmailService created")

email_service.send_ticket_email(
    to_email="your_test_email@gmail.com",
    subject="Test Email",
    message_body="Email system working!"
)

print("✅ DONE")