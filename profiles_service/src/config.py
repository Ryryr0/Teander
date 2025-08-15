from functools import cached_property

from aiokafka import AIOKafkaConsumer
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file="C:/Users/artem/Desktop/traineeship/pet_project/Teander/profiles_service/.env"
    )  # does not need in docker

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
    KAFKA_PUBLIC_KEY_TOPIC: str = ""
    KAFKA_PUBLIC_KEY_GROUP: str = ""

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
    
    async def get_public_key(self):
        consumer = AIOKafkaConsumer(
            self.KAFKA_PUBLIC_KEY_TOPIC,
            bootstrap_servers=self.KAFKA_BOOTSTRAP_SERVERS,
            group_id=self.KAFKA_PUBLIC_KEY_GROUP,
        )
        await consumer.start()
        try:
            async for msg in consumer:
                if isinstance(msg.value, bytes):
                    self._public_key = msg.value.decode()
        finally:
            await consumer.stop()

    # @property
    # def PUBLIC_KEY(self) -> str:
    #     return """
    #     -----BEGIN PUBLIC KEY-----
    #     MIIBIjANBgkqhkiG9w0BAQEFAAOCAQ8AMIIBCgKCAQEAyrt9oclp166oK5lB0jmy
    #     N1FwiO1vgO9HGJgLD59UXRjJgEuoP0HYBNgmoOAFNMRp8C5Tgog+NCGEn8+CoGSD
    #     WJU6Mb/HHnK+p8Q/SflbRkLPobJcW7k17+InpNiJzDsOpS6GT845+1Z2k03nacLl
    #     Ni2jLfD0pv3TdZWEH7IK1OeX5koEqIPwRtAPSbc6zSzE1GfxPm9+g6md633rwGpz
    #     dvG9djm1m+6yVirKE9iTr2Zy5G5unIHLKxmQ0q8Pp0PIiUjK2iw5F9lMaIICIOp0
    #     HYgdoaq9Rmy3KAVUHebuQosAONdXFFx/4LXarSqmoeS/z1M4mJijIHdKofmQGVBs
    #     SQIDAQAB
    #     -----END PUBLIC KEY-----
    #     """


settings = Settings()
