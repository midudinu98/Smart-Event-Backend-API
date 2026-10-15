from fastapi import APIRouter, WebSocket, WebSocketDisconnect
from app.utils.connection_manager import manager

router = APIRouter(tags=["Real-Time Updates"])

@router.websocket("/ws/events/{event_id}")
async def event_availability_websocket(websocket: WebSocket,event_id: int):
    await manager.connect(event_id, websocket)

    try:
        while True:
            # Keep the connection alive
            await websocket.receive_text()

    except WebSocketDisconnect:
        manager.disconnect(event_id, websocket)

    except Exception:
        manager.disconnect(event_id, websocket)
