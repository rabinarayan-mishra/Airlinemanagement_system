# modules/whatsapp_service.py

import webbrowser
import urllib.parse


class WhatsAppService:

    @staticmethod
    def send_message(phone, message):

        phone = str(phone).strip()

        # Remove spaces
        phone = phone.replace(" ", "")

        # Add India code if missing
        if not phone.startswith("91"):
            phone = "91" + phone

        url = f"https://wa.me/{phone}?text={urllib.parse.quote(message)}"

        webbrowser.open(url)