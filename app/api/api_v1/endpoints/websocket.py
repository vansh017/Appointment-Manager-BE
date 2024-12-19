from fastapi import FastAPI, WebSocket, WebSocketDisconnect, APIRouter
from typing import List, Dict

ws = APIRouter(
    prefix="/ws"
)


class ConnectionManager:
    def __init__(self):
        self.active_connections: List[WebSocket] = []
        self.shop_connections: Dict[int, List[WebSocket]] = {}

    async def connect(self, websocket: WebSocket, shop_id: int):
        print("connected")
        await websocket.accept()
        self.active_connections.append(websocket)

        if shop_id not in self.shop_connections:
            self.shop_connections[shop_id] = []
        self.shop_connections[shop_id].append(websocket)
        print(self.shop_connections)

    def disconnect(self, websocket: WebSocket, shop_id: int):
        self.active_connections.remove(websocket)
        self.shop_connections[shop_id].remove(websocket)

    async def broadcast_to_shop(self, message: dict, shop_id: int):
        for connection in self.shop_connections.get(shop_id, []):
            await connection.send_json(message)


connection_manager = ConnectionManager()


@ws.websocket("/queue/{shop_id}")
async def websocket_queue_endpoint(websocket: WebSocket, shop_id: int):
    await connection_manager.connect(websocket, shop_id)
    try:
        while True:
            data = await websocket.receive_json()


            # Handle incoming messages if needed
            await connection_manager.broadcast_to_shop(data, shop_id)
    except WebSocketDisconnect:

        connection_manager.disconnect(websocket, shop_id)
    except Exception as e:
        print(e)