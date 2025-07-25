import logging
import json
import sys


class JsonFormatter(logging.Formatter):
    def format(self, record):
        log_record = {
            "timestamp": self.formatTime(record),
            "level": record.levelname,
            "name": record.name,
            "message": record.getMessage(),
            "request_id": getattr(record, "request_id", "N/A"),
        }
        return json.dumps(log_record)


class Logger:
    __handler = logging.StreamHandler(sys.stdout)
    __handler.setFormatter(JsonFormatter())

    __logger = logging.getLogger("auth_service")
    __logger.setLevel(logging.DEBUG)
    __logger.addHandler(__handler)

    __counter = 0

    @classmethod
    def __get_count_log(cls, message: str, request_id: int | None = None) -> dict[str: str, dict, None]:
        if request_id:
            return {"message": message, "extra": {"request_id": request_id}}
        else:
            cls.__counter += 1
            return {"message": message, "extra": {"request_id": cls.__counter}}

    @classmethod
    def log_request(cls, message: str, request_id: int | None = None) -> int | None:
        data = cls.__get_count_log(message, request_id)
        cls.__logger.info(data["message"], extra=data["extra"])
        if data["extra"]:
            return data["extra"]["request_id"]

    @classmethod
    def info(cls, message: str):
        cls.__logger.info(message)

    @classmethod
    def error(cls, message: str):
        cls.__logger.error(message)

    @classmethod
    def warning(cls, message: str):
        cls.__logger.warning(message)

    @classmethod
    def critical(cls, message: str):
        cls.__logger.critical(message)

    @classmethod
    def debug(cls, message: str):
        cls.__logger.debug(message)
