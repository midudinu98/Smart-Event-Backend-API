# Smart-Event-Backend-API

# SmartEvent – Event Discovery & Ticket Booking System

# Overview

SmartEvent is a backend event discovery and ticket booking system developed using Python and FastAPI. It provides REST APIs for user authentication, event discovery, ticket booking, QR-code ticket generation, payment processing, notifications, event management, and administrator analytics.

The system includes 24 modules covering authentication, event management, booking, payments, recommendations, advanced filtering, and an AI chatbot assistant.

# Project Overview

SmartEvent is a backend API for an event discovery and ticket booking system developed using FastAPI.

**The application allows users to:**

* Register and log in securely using JWT authentication
* Browse and search events by title, category, location, and date
* Book tickets and view booking history
* Generate QR-code tickets and verify ticket information
* Make simulated payments for bookings
* Apply coupons and discounts
* Submit event reviews and ratings
* Manage wishlists and user profiles
* Receive booking notifications, event reminders, and announcements
* Get personalized event recommendations
* Access real-time ticket availability updates
* Interact with an AI chatbot for event discovery, booking information, and ticket support

**The system also provides Organizer functionality to:**

* Create and manage events
* Update event information and status
* Manage organizer-owned events
* Publish event announcements
* Monitor event activity

**The system also provides Admin functionality to:**

* Manage events and oversee registered users
* View events and bookings across the platform
* Track total tickets sold and bookings
* View platform revenue summaries
* Monitor daily ticket sales
* Analyze monthly booking trends
* Identify the most popular events
* Identify top revenue-generating events
* Manage platform operations through role-based access control

The application uses FastAPI, Python, SQLAlchemy, SQLite, JWT authentication, and Pydantic to provide secure, structured, and scalable backend APIs.

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
│ │ │ ├── __init__.py <br>
│ │ │ ├── user.py <br>
│ │ │ ├── events.py <br>
│ │ │ ├── booking.py<br>
│ │ │ ├── tickets.py <br>
│ │ │ └── notification.py <br>
│ │ │ └── coupon.py <br>
│ │ │ └── payment.py <br>
│ │ │ └── review.py <br>
│ │ │ ├── event_update.py <br>
│ │ │ ├── event_view.py <br>
│ │ │ ├── wishlist.py <br>
│ <br>
│ │ ├── routers/ <br>
│ │ │ ├── __init__.py <br>
│ │ │ ├── auth.py <br>
│ │ │ ├── event.py <br>
│ │ │ ├── booking.py <br>
│ │ │ ├── ticket.py <br>
│ │ │ ├── notification.py <br>
│ │ │ └── admin.py <br>
│ │ │ └── user.py <br>
│ │ │ └── analytics.py <br>
│ │ │ └── admin_analytics.py <br>
│ │ │ └── coupon.py <br>
│ │ │ └── payment.py <br>
│ │ │ └── review.py <br>
│ │ │ ├── event_update.py <br>
│ │ │ ├── event_recommendations.py <br>
│ │ │ ├── wishlist.py <br>
│ │ │ ├── realtime.py <br>
│ │ │ ├── charbot.py <br>
│<br>
│ │ ├── schemas/ <br>
│ │ │ ├── user.py <br>
│ │ │ ├── events.py <br>
│ │ │ ├── booking.py <br>
│ │ │ ├── ticket.py <br>
│ │ │ └── notification.py <br>
│ │ │ └── analytics.py <br>
│ │ │ └── coupon.py <br>
│ │ │ └── payment.py <br>
│ │ │ └── review.py <br>
│ │ │ ├── wishlist.py <br>
│ │ │ ├── event_update.py <br>
│ │ │ ├── charbot.py <br>
│<br>
│ │ ├── utils/ <br>
│ │ │ ├── security.py <br>
│ │ │ ├── ticket.py <br>
│ │ │ ├── qr_code.py <br>
│ │ │ └── notification.py <br>
│ │ │ └── event_status.py <br>
│<br>
│ | ├── config.py  <br>
│ | ├── database.py <br>
│ | │── chatbot_service.py  <br>
│ | │── main.py  <br>
|<br>
| ├── .env <br>
| ├── .gitignore <br>
│ ├── requirements.txt <br>
│ ├── migrate.py.txt <br>
│ ├── check_notfy.py.txt <br>
| ├── smartevent.db <br>
| ├── smarteventBackup.db <br>
│ └── README.md <br>
│<br>
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

## Module 1: User Authentication & JWT
* User registration and login
* Password hashing
* JWT access token generation and validation
* Protected API endpoints
* User profile access

## Module 2: Event Discovery
* Retrieve available events
* Search events by title
* Filter events by category
* View event information

## Module 3: Ticket Booking
* Create ticket bookings
* Calculate total booking price
* Track booking status
* Retrieve booking information

## Module 4: QR Code Ticket System
* Generate QR codes for tickets
* Associate tickets with bookings
* Retrieve ticket information

## Module 5: Event Reminder Notifications
* Booking confirmation notifications
* Upcoming event reminders
* Retrieve user-specific notifications

## Module 6: Admin Authorization
* Role-based access control (RBAC)
* Protect administrator-only endpoints
* Restrict operations according to user roles

## Module 7: Admin Event Management
* Create events
* Update event information
* Manage event operations
* Apply role-based authorization

#Module 8: Admin Dashboard
* Provide administrative API endpoints
* Retrieve platform information
* Support administrative monitoring

## Module 9: Booking Statistics
* Retrieve booking statistics
* Track booking status
* Calculate booking totals

## Module 10: Event Status & Updates
* Update event information
* Manage event status
* Protect event update operations using role-based authorization

## Module 11: Admin Dashboard & Platform Analytics
* Total registered users
* Total events created
* Total tickets sold
* Total bookings
* Platform revenue summary
* Daily ticket sales
* Monthly booking trends
* Most popular events
* Top revenue-generating events
* View all users
* View all events
* View all bookings

## Module 12: Event Payment System
* Simulate event ticket payments
* Create payment records for bookings
* Track payment status
* Store transaction IDs and payment amounts
* Update booking status after successful payment

## Module 13: Coupon & Discount System
* Apply coupon codes to bookings
* Validate coupon eligibility
* Calculate discounts
* Apply discounted booking prices

## Module 14: Event Feedback & Rating System
* Submit event feedback and ratings
* Associate feedback with users and events
* Retrieve event reviews and ratings

## Module 15: Notification System Enhancements
* Enhance user notification functionality
* Manage notification records
* Support booking and event-related notifications

## Module 16: Event Search & Filtering Improvements
* Improve event search functionality
* Support event filtering
* Improve event discovery API capabilities

## Module 18: Real-Time Event Availability
* Track available event tickets
* Update ticket availability after bookings
* Support real-time updates through WebSockets or polling

Module 19: Personalized Event Recommendations
* Recommend events based on user activity
* Consider viewed and booked event categories
* Improve recommendations using location and popularity

## Module 20: Wishlist System
* Allow users to add events to their wishlists
* Support removing events from wishlists
* Retrieve saved events

## Module 21: Live Event Updates & Announcements
* Allow organizers and administrators to publish announcements
* Store event-related updates
* Provide APIs to retrieve event announcements

## Module 22: User Profile Enhancements
* Implement user profile updates
* Support optional profile picture uploads
* Provide booking summaries

## Module 23: Advanced Event Search & Filtering
* Support filtering by category, price, date, and location
* Allow multiple filters in a single search
* Validate invalid filter criteria

## Module 24: AI Chatbot Assistant
* Implement an API endpoint for chatbot interactions
* Assist with event discovery and music event queries
* Provide booking information and ticket-related support
* Support authenticated user requests
