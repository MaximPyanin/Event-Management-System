from fastapi import APIRouter, HTTPException
from sqlalchemy import select

from app.database.db import DB


class HealthcheckRouter:
    def __init__(self, db: DB):
        self.db = db
        self.router = APIRouter(prefix="/api/v1", tags=["healthcheck"])

    def get_router(self) -> APIRouter:
        self.router.get("/health")(self.check_connection)
        return self.router

    async def check_connection(self) -> dict:
        try:
            async with self.db.get_engine().connect() as connection:
                await connection.execute(select(1))
            return {"status": "ok"}
        except Exception:
            raise HTTPException(status_code=500, detail="Database connection error")
