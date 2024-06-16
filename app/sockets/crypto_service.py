import asyncio

from app.sockets.websocket_service import WebsocketService
from fastapi import WebSocket, WebSocketDisconnect
from httpx import AsyncClient


class CryptoService:
    def __init__(self, websocket_service: WebsocketService):
        self.websocket_service = websocket_service
        self.async_client = AsyncClient()

    async def crypto_rates(self, websocket: WebSocket) -> None:
        await self.websocket_service.connect(websocket)
        try:
            while True:
                data = await self.get_rates()
                await self.websocket_service.send_personal_message(data, websocket)
                await asyncio.sleep(1)
        except WebSocketDisconnect:
            self.websocket_service.disconnect(websocket)

    async def get_rates(self) -> dict:
        response = await self.async_client.get(
            "https://api.binance.com/api/v3/ticker/price?symbol=BTCUSDT"
        )
        return response.json()
