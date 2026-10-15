from fastapi import FastAPI

from app.database import Base,engine

from app import models

from app.routers import (auth_router,
    user_router,
    events_router,
    booking_router,
    notification_router,
    admin_router,
    analytics_router,
    admin_analytics_router,
    payment_router,
    coupon_router,
    review_router,
    realtime_router,
    ER_router,
    wishlist_router,
    event_updates,
    chatbot)

from fastapi.staticfiles import StaticFiles

import asyncio

from app.database import SessionLocal
from app.utils.notification import create_event_reminders

Base.metadata.create_all(bind=engine)

app=FastAPI(title="SMART EVENT BACKEND API",description="Event Discovery & Ticket Booking System.",version="1.0.0")

async def reminder_loop():

    while True:

        db = SessionLocal()

        try:
            create_event_reminders(db)
        finally:
            db.close()

        await asyncio.sleep(3600)

app.mount("/static", StaticFiles(directory="static"), name="static")

app.include_router(auth_router)
app.include_router(user_router)
app.include_router(events_router)
app.include_router(booking_router)
app.include_router(notification_router)
app.include_router(admin_router)
app.include_router(analytics_router)
app.include_router(admin_analytics_router)
app.include_router(payment_router)
app.include_router(coupon_router)
app.include_router(review_router)
app.include_router(realtime_router)
app.include_router(ER_router)
app.include_router(wishlist_router)
app.include_router(event_updates)
app.include_router(chatbot)

@app.get("/")
def root():
    return{"message": "API IS RUNNING"}

@app.on_event("startup")
async def startup_event():
    asyncio.create_task(reminder_loop())

@app.get("/health")
def health_check():
    return{"status": "HEALTHY"}