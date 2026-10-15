from sqlalchemy.orm import Session
from app.models.events import Event
from app.models.booking import Booking

def get_chatbot_reply(message: str,db: Session,user_id: int) -> str:

    query = message.lower().strip()

    if not query:
        return "Please enter a message."

    # Find nearby events
    if "near me" in query or "nearby" in query:
        return ("Please provide your city or location so "
            "I can help you find relevant events.")

    # Find music events
    if "music" in query and ("event" in query or "weekend" in query):
        
        events = (db.query(Event).filter(Event.category.ilike("%music%")).limit(5).all())

        if not events:
            return "No music events were found."

        results = ["Here are some music events:"]

        for event in events:
            results.append(f"- {event.title}")

        return "\n".join(results)

    # Show the logged-in user's bookings
    if "booking" in query:
        
        bookings = (db.query(Booking).filter(Booking.user_id == user_id).order_by(Booking.created_at.desc()).limit(10).all())

        if not bookings:
            return "You don't have any bookings yet."

        results = ["Here are your recent bookings:"]

        for booking in bookings:
            results.append(f"- Booking ID: {booking.id}, "f"Status: {booking.status}")

        return "\n".join(results)

    # Ticket support
    if "ticket" in query:
        return ("For ticket issues, check your booking status "
            "and ticket QR code. If the issue continues, "
            "contact the event organizer or support team.")

    # Greeting
    if any(word in query for word in ["hello", "hi"]):
        return ("Hello! Welcome to SmartEvent. "
            "Ask me about events, bookings, or ticket issues.")

    return ("I can help you discover music events, "
        "check your bookings, and troubleshoot ticket issues.")
