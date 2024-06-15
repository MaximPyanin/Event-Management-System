from fastapi import APIRouter,WebSocket

from app.sockets.crypto_service import CryptoService


class WebsocketRouter:
    def __init__(self,crypto_service: CryptoService):
        self.router = APIRouter(tags=['websocket'])
        self.crypto_service = crypto_service
    def get_router(self) -> APIRouter:
        self.router.websocket('/stream')(self.get_crypto_currencies)
        return self.router

    async def get_crypto_currencies(self,websocket: WebSocket):
        await self.get_crypto_currencies(websocket)
