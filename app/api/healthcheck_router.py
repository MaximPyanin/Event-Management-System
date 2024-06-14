from fastapi import APIRouter


class HealthcheckRouter:
    def __init__(self):
        self.router = APIRouter(prefix="/api/v1", tags=["healthcheck"])

    def get_router(self) -> APIRouter:
        self.router.get("/health")(self.check_connection)
        return self.router

    async def check_connection(self) -> dict:
        return {"status": "ok"}
