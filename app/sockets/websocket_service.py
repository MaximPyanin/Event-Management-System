from fastapi import  WebSocket,WebSocketDisconnect
import requests

class WebsocketService:
    def __init__(self):
        self.active_connections: list[WebSocket] = []

    async def connect(self, websocket: WebSocket):
        await websocket.accept()
        self.active_connections.append(websocket)

    def disconnect(self, websocket: WebSocket):
        self.active_connections.remove(websocket)

    async def send_personal_message(self, message: str, websocket: WebSocket):
        await websocket.send_text(message)

    async def broadcast(self, message: str):
        for connection in self.active_connections:
            await connection.send_text(message)

    async def crypto_rates(self,websocket: WebSocket) -> None:
        await self.connect(websocket)
        try:
            while True:
                data = self.get_rates()
                await self.broadcast(data)
        except WebSocketDisconnect:
            self.disconnect(websocket)

    def get_rates(self):

        key = "https://api.binance.com/api/v3/ticker/price?symbol=BTCUSDT"

        data = requests.get(key)
        data = data.json()
        return data['price']
