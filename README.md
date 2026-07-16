#  ✈ Airlinemanagement_system

📖 Project Overview
The Airline Management System is a desktop-based application developed using Python, Tkinter, and MySQL. It is designed to simplify airline reservation and passenger management by providing an intuitive graphical interface for administrators. The system automates passenger registration, flight booking, seat allocation, boarding pass generation, ticket cancellation, and journey management while maintaining all records securely in a MySQL database.
The application follows a modular architecture where each module is responsible for a specific operation, making the system scalable, maintainable, and easy to understand. It also integrates Email and WhatsApp notification services to provide real-time booking confirmations, offering a practical simulation of a modern airline reservation system.

⸻

🎯 Objectives
* Automate airline reservation processes.
* Reduce manual work in passenger management.
* Maintain passenger and booking records securely.
* Provide a simple and user-friendly graphical interface.
* Demonstrate real-world database operations using Python.

⸻

🛠️ Technology Stack
Technology	Purpose
Python	Application Development
Tkinter	Graphical User Interface
MySQL	Database Management
mysql-connector-python	Database Connectivity
SMTP	Email Notifications
WhatsApp API	Booking Notifications
Git & GitHub	Version Control
⸻

📂 Project Structure
AirlineManagementSystem/
│
├── main.py
├── db.py
├── login.py
│
├── modules/
│   ├── add_customer.py
│   ├── book_flight.py
│   ├── boarding_pass.py
│   ├── cancel_ticket.py
│   ├── journey_details.py
│   ├── flight_info.py
│   ├── email_service.py
│   └── whatsapp_service.py
│
├── database/
│   └── airline.sql
│
└── assets/
    ├── images/
    └── icons/

⸻

🔐 Login Module
The Login Module authenticates administrators before granting access to the system. User credentials are verified against the MySQL database to ensure only authorized users can access airline operations. This module serves as the security layer of the application.
Features
* Username & Password Authentication
* Database Validation
* Invalid Login Detection
* Secure Access

⸻

## 👤 Add Passenger Module
The Add Passenger module allows administrators to register new passengers by entering personal information such as name, gender, phone number, email, nationality, Aadhaar number, and passport number. All records are validated and stored securely in the MySQL database.
Features
* Passenger Registration
* Data Validation
* MySQL Storage
* Duplicate Record Prevention

## 👤 Add Passenger

![Add Passenger Form](https://raw.githubusercontent.com/rabinarayan-mishra/Airlinemanagement_system/main/airlinemanagementsystem/assets/add_passenger_1.png)

### Passenger Registration

![Passenger Registration](https://raw.githubusercontent.com/rabinarayan-mishra/Airlinemanagement_system/main/airlinemanagementsystem/assets/add_passenger_2.png)
⸻

## ✈ Book Flight Module
The Book Flight module enables administrators to search passengers using their Aadhaar number and book flights based on the selected source and destination. The system automatically allocates seats, generates a unique PNR, stores booking information, and sends confirmation through Email and WhatsApp.
Features
* Passenger Search
* Flight Search
* Automatic Seat Allocation
* Unique PNR Generation
* Booking Confirmation
* Email Notification
* WhatsApp Notification
## ✈️ Book Flight

### Flight Booking Form

![Book Flight Form](https://raw.githubusercontent.com/rabinarayan-mishra/Airlinemanagement_system/main/airlinemanagementsystem/assets/book_flight_1.png)

### Booking Confirmation

![Book Flight](https://raw.githubusercontent.com/rabinarayan-mishra/Airlinemanagement_system/main/airlinemanagementsystem/assets/BOOK%20FLIGHT2.png)
⸻

## 🛫 Flight Information Module
This module displays available flights, including flight ID, flight name, source, destination, departure schedule, arrival schedule, and seat availability. It helps administrators quickly retrieve flight information.
Features
* Flight Search
* Route Information
* Flight Details
* Seat Availability
## 🛫 Flight Information

### Available Flights & Route Details

![Flight Information](https://raw.githubusercontent.com/rabinarayan-mishra/Airlinemanagement_system/main/airlinemanagementsystem/assets/flight_information.png)

⸻

## 🎫 Boarding Pass Module
After a successful booking, the Boarding Pass module generates the passenger’s boarding pass containing essential travel details such as passenger information, flight information, seat number, booking status, and PNR.
Features
* Boarding Pass Generation
* Passenger Details
* Flight Information
* PNR Display
## 🎫 Boarding Pass

### Passenger Boarding Pass

![Boarding Pass](https://raw.githubusercontent.com/rabinarayan-mishra/Airlinemanagement_system/main/airlinemanagementsystem/assets/boarding_pass.png)
⸻

## 📋 Journey Details Module
The Journey Details module provides a complete overview of booked journeys. It retrieves booking records from the database and displays travel information, allowing administrators to verify reservations easily.
Features
* Booking History
* Passenger Details
* Flight Details
* Journey Information
## 🧳 Journey Details

### Passenger Journey & Booking History

![Journey Details](https://raw.githubusercontent.com/rabinarayan-mishra/Airlinemanagement_system/main/airlinemanagementsystem/assets/journey_details.png)
⸻

## ❌ Cancel Ticket Module
The Cancel Ticket module enables administrators to cancel confirmed bookings using the generated PNR. Once cancelled, the booking status is updated in the database and the allocated seat becomes available again.
Features
* Ticket Cancellation
* PNR Verification
* Database Update
* Seat Release
## ❌ Cancel Ticket

### Cancel Ticket Form

![Cancel Ticket Form](https://raw.githubusercontent.com/rabinarayan-mishra/Airlinemanagement_system/main/airlinemanagementsystem/assets/cancel_ticket_1.png)

### Cancellation Confirmation

![Cancellation Confirmation](https://raw.githubusercontent.com/rabinarayan-mishra/Airlinemanagement_system/main/airlinemanagementsystem/assets/cancel_ticket_2.png)
⸻

## 📧 Email Notification Module
This module automatically sends booking confirmation emails to passengers immediately after successful reservation. The email contains booking information including PNR, seat number, flight details, and booking status.
Features
* Automatic Email
* Booking Summary
* Confirmation Notification
## 📧 Email Confirmation

### Booking Confirmation Email

![Email Confirmation](https://raw.githubusercontent.com/rabinarayan-mishra/Airlinemanagement_system/main/airlinemanagementsystem/assets/email_confirmation.png)
⸻

## 💬 WhatsApp Notification Module
The WhatsApp integration sends instant booking confirmations directly to the passenger’s registered mobile number, improving communication and user experience.
Features
* Instant Notification
* Booking Confirmation
* Passenger Communication
## 💬 WhatsApp Notification

### Instant Booking Notification

![WhatsApp Notification](https://raw.githubusercontent.com/rabinarayan-mishra/Airlinemanagement_system/main/airlinemanagementsystem/assets/whatsapp_notification.png)
⸻

🗄️ Database
The project uses MySQL to manage all application data.
Tables
* Login
* Passenger
* Flights
* Bookings
The database maintains relationships between passengers, flights, and bookings, ensuring consistency and efficient data retrieval.

⸻

🔄 Project Workflow
Login
   │
   ▼
Dashboard
   │
   ├── Add Passenger
   │
   ├── Book Flight
   │      │
   │      ├── Search Passenger
   │      ├── Search Flight
   │      ├── Allocate Seat
   │      ├── Generate PNR
   │      ├── Save Booking
   │      ├── Send Email
   │      └── Send WhatsApp
   │
   ├── Boarding Pass
   │
   ├── Journey Details
   │
   ├── Cancel Ticket
   │
   └── Flight Information

⸻

🚀 Future Improvements
* Online Payment Gateway
* QR Code Boarding Pass
* Live Flight Tracking
* Multi-user Authentication
* Admin Dashboard Analytics
* PDF Ticket Generation
* Passenger Self Check-in
* Cloud Database Deployment
