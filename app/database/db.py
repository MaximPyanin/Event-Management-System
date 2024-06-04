from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker, AsyncEngine

from app.services.config_service import AppConfig


class DB:
    def __init__(self, config: AppConfig):
        self.__engine = create_async_engine(
            url=config.POSTGRES_URI, isolation_level="AUTOCOMMIT"
        )

    def get_sessionmaker(self) -> async_sessionmaker:
        return async_sessionmaker(bind=self.__engine)

    def get_engine(self) -> AsyncEngine:
        return self.__engine
