import os
from functools import cached_property

from aiokafka import AIOKafkaConsumer
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    if os.environ.get("IS_DOCKER") == "false":
        model_config = SettingsConfigDict(
            env_file="profiles_service/.env"
        )

    # PostgresSQL db
    DB_HOST: str = ""
    DB_PORT: int = 0
    DB_USER: str = ""
    DB_PASS: str = ""
    DB_NAME: str = ""

    # Redis cache
    REDIS_HOST: str = ""
    REDIS_PORT: int = 0
    REDIS_PASSWORD: str = ""

    # Logger
    LOG_LVL: str = ""

    # Kafka
    KAFKA_BOOTSTRAP_SERVERS: str = ""
    # Groups
    KAFKA_GROUP: str = ""
    # Topics
    KAFKA_PUBLIC_KEY_TOPIC: str = ""
    KAFKA_USERS_TOPIC: str = ""

    # Sites allowed to do requests
    ORIGINS: list[str] = ["*"]

    # For jwt token
    ALGORITHM: str = ""
    _public_key = ""

    @cached_property
    def DATABASE_URL(self) -> str:
        """URl for sqlalchemy connection"""
        return f"postgresql+asyncpg://{self.DB_USER}:{self.DB_PASS}@{self.DB_HOST}:{self.DB_PORT}/{self.DB_NAME}"

    @property
    def PUBLIC_KEY(self) -> str:
        """Public key for jwt decoding"""
        return self._public_key
    
    async def get_public_key(self) -> bool:
        consumer = AIOKafkaConsumer(
            self.KAFKA_PUBLIC_KEY_TOPIC,
            bootstrap_servers=self.KAFKA_BOOTSTRAP_SERVERS,
        )
        await consumer.start()
        try:
            async for msg in consumer:
                if isinstance(msg.value, bytes):
                    self._public_key = msg.value.decode()
                    break
        finally:
            await consumer.stop()
        return bool(self._public_key)

settings = Settings()
