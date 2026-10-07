# Smart-Event-Backend-API

# SmartEvent – Event Discovery & Ticket Booking System

# Overview

SmartEvent is a backend API for an event discovery and ticket booking system developed using FastAPI.

The application provides secure user authentication, event management, ticket booking, QR-code ticket generation, notifications, event reminders, and admin management.

# Project Overview

SmartEvent is an event discovery and ticket booking backend application built using FastAPI.

The system allows users to:

* Register and log in
* Browse events
* Search events by title
* Filter events by category
* Book tickets  
* View booking history
* Generate QR-code tickets
* View their tickets
* Receive booking confirmation notifications
* Receive upcoming event reminders

The system also provides Admin functionality for managing events and viewing system statistics.

# Technology Stack

* Python
* FastAPI
* SQLAlchemy
* SQLite
* Pydantic
* JWT Authentication
* Password Hashing with bcrypt
* QR Code Generation
* Uvicorn
* SQLite

Smart_Event/ <br>
│  <br>
│  <br>
│ ├── app/ <br>
│ │ ├── models/ <br>
│ │ │ ├── user.py <br>
│ │ │ ├── events.py <br>
│ │ │ ├── booking.py<br>
│ │ │ ├── tickets.py <br>
│ │ │ └── notification.py <br>
│ <br>
│ │ ├── routers/ <br>
│ │ │ ├── auth.py <br>
│ │ │ ├── event.py <br>
│ │ │ ├── booking.py <br>
│ │ │ ├── ticket.py <br>
│ │ │ ├── notification.py <br>
│ │ │ └── admin.py <br>
│<br>
│ │ ├── schemas/ <br>
│ │ │ ├── user.py <br>
│ │ │ ├── events.py <br>
│ │ │ ├── booking.py <br>
│ │ │ ├── ticket.py <br>
│ │ │ └── notification.py <br>
│<br>
│ │ ├── utils/ <br>
│ │ │ ├── security.py <br>
│ │ │ ├── ticket.py <br>
│ │ │ ├── qr_code.py <br>
│ │ │ └── notification.py <br>
│<br>
│ ├── config.py  <br>
│ ├── database.py <br>
│ │── main.py  <br>
| ├── .env <br>
| ├── .gitignore <br>
│ ├── requirements.txt  <br>
| ├── smartevent.db  <br>
│ └── README.md   <br>
│  <br>
└── ... 

# Installation

## 1. Create virtual environment

**python -m venv venv**

## 2. Activate virtual environment

**.\venv\Scripts\Activate**

## 3. Install dependencies

**pip install -r requirements.txt**

## 4. Configure environment variables

Create a .env file:

**DATABASE_URL=sqlite:///./smart_event.db** <br>
**SECRET_KEY=your-secret-key**  <br>
**ALGORITHM=HS256**  <br>
**ACCESS_TOKEN_EXPIRE_MINUTES=60**  <br>

Do not commit the .env file or real secret keys to GitHub.

# Run the Application

From the backend directory:

**uvicorn app.main:app --reload**

The API will run at:

**http://127.0.0.1:8000**

# API Documentation

Swagger UI

**http://127.0.0.1:8000/docs**

Swagger UI can be used to test and explore all available APIs.

# Security

The project implements:

* JWT authentication
* Password hashing
* Protected routes
* Role-based access control
* Admin-only event management
* User-specific bookings
* User-specific tickets
* User-specific notifications
* Password hash protection in admin user responses

# Modules Completed

1. ✅ Authentication & JWT
2. ✅ Event Discovery
3. ✅ Ticket Booking
4. ✅ QR Code Ticket System
5. ✅ Event Reminder Notifications
6. ✅ Admin Authorization
7. ✅ Admin Event Management
8. ✅ Admin Dashboard
9. ✅ Booking Statistics
10. ✅ Ticket Statistics
11. ✅ Revenue Statistics
12. ✅ Admin User Management
13. ✅ Admin Booking Management
14. ✅ Admin Event Management  

