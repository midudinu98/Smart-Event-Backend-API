from pydantic import BaseModel

class EventAnalyticsResponse(BaseModel):
    event_id: int
    event_title: str
    total_tickets_sold: int
    remaining_tickets: int
    total_revenue: float
    booking_count: int