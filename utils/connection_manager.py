from fastapi import WebSocket
from typing import Dict, List

class ConnectionManager:
    def __init__(self):
        self.active_connections: Dict[int, List[WebSocket]] = {}

    async def connect(self, event_id: int, websocket: WebSocket):
        await websocket.accept()

        if event_id not in self.active_connections:
            self.active_connections[event_id] = []

        self.active_connections[event_id].append(websocket)

    def disconnect(self, event_id: int, websocket: WebSocket):
        if event_id in self.active_connections:
            if websocket in self.active_connections[event_id]:
                self.active_connections[event_id].remove(websocket)

            if not self.active_connections[event_id]:
                del self.active_connections[event_id]

    async def broadcast(self, event_id: int, message: dict):
        connections = self.active_connections.get(event_id, []).copy()

        for connection in connections:
            try:
                await connection.send_json(message)
            except Exception:
                self.disconnect(event_id, connection)

manager = ConnectionManager()
