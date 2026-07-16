# Airlinemanagement_system
# 📸 Application Screenshots

---

## 👤 Add Passenger

The **Add Passenger** module allows administrators to register new passengers by entering details such as full name, gender, phone number, email address, nationality, Aadhaar number, and passport number. The information is validated and stored securely in the MySQL database.

### Add Passenger Form

![Add Passenger](assets/images/add_passenger_1.png)

### Passenger Registration

![Passenger Registration](assets/images/add_passenger_2.png)

---

## ✈ Book Flight

The **Book Flight** module allows administrators to search passengers using their Aadhaar number, retrieve available flights based on source and destination, and complete reservations. The system automatically generates a unique PNR, assigns a seat number, and stores the booking in the database.

### Passenger & Flight Search

![Book Flight](assets/images/book_flight_1.png)

### Booking Confirmation

![Booking Confirmation](assets/images/book_flight_2.png)

---

## 🛫 Flight Information

This module displays available flight information including flight ID, flight name, source, destination, and other details stored in the database.

![Flight Information](assets/images/flight_information.png)

---

## 📋 Journey Details

The Journey Details module allows administrators to retrieve and view booked journey information using passenger or booking details.

![Journey Details](assets/images/journey_details.png)

---

## 🎫 Boarding Pass

After a successful booking, the Boarding Pass module generates a boarding pass containing passenger details, PNR number, seat number, and flight information.

![Boarding Pass](assets/images/boarding_pass.png)

---

## ❌ Cancel Ticket

The Cancel Ticket module enables administrators to search for an existing booking using its PNR and cancel the reservation. The booking status is updated in the database, making the seat available again.

### Search Ticket

![Cancel Ticket](assets/images/cancel_ticket_1.png)

### Ticket Cancelled

![Ticket Cancelled](assets/images/cancel_ticket_2.png)

---

## 📧 Email Confirmation

After a successful booking, the system automatically sends a confirmation email containing the passenger's booking details, PNR number, flight information, seat number, ticket price, and booking status.

![Email Confirmation](assets/images/email_confirmation.png)

---

## 💬 WhatsApp Notification

The system also sends an instant WhatsApp notification to the passenger containing the booking confirmation and important travel details.

![WhatsApp Notification](assets/images/whatsapp_notification.png)
