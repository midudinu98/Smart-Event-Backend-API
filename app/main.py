from fastapi import FastAPI

from app.database import Base,engine

from app.models.user import User
from app.models.events import Event
from app.models.booking import Booking
from app.models.tickets import Ticket

from app.routers.auth import router as auth_router
from app.routers.user import router as user_router
from app.routers.events import router as events_router
from app.routers.booking import router as booking_router
from app.routers.notification import router as notification_router
from app.routers.admin import router as admin_router


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

@app.get("/")
def root():
    return{"message": "API IS RUNNING"}

@app.on_event("startup")
async def startup_event():
    asyncio.create_task(reminder_loop())

@app.get("/health")
def health_check():
    return{"status": "HEALTHY"}