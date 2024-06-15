from fastapi import APIRouter,WebSocket

from app.sockets.websocket_service import WebsocketService


class WebsocketRouter:
    def __init__(self,websocket_service: WebsocketService):
        self.router = APIRouter(tags=['websocket'])
        self.websocket_service = websocket_service
    def get_router(self) -> APIRouter:
        self.router.websocket('/stream')(self.get_crypto_currencies)
        return self.router

    async def get_crypto_currencies(self,websocket: WebSocket):
        await self.websocket_service.crypto_rates(websocket)
