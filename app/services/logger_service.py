from logging.handlers import SysLogHandler
from logging import getLogger
from logging import INFO
from logging import Formatter
from app.services.config_service import AppConfig


class LoggerService:
    def __init__(self, config: AppConfig):
        self.logger = getLogger(__name__)
        self.logger.setLevel(INFO)
        self.config = config

    def set_handler(self) -> None:
        handler = SysLogHandler(
            address=(self.config.PAPERTRAIL_HOST, self.config.PAPERTRAIL_PORT)
        )
        formatter = Formatter("%(asctime)s %(levelname)s %(message)s")
        handler.setFormatter(formatter)
        self.logger.addHandler(handler)

    def start_logging(self):
        return self.logger.info("logging started")
