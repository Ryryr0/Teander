from aiokafka import AIOKafkaProducer

from schemas import UsersSendDTO
from interfaces import ISynchronizer
from config import settings


class Synchronizer(ISynchronizer):
    def __init__(self):
        self.__producer = AIOKafkaProducer(
            bootstrap_servers=settings.KAFKA_BOOTSTRAP_SERVERS,
            enable_idempotence=True,
        )

    async def send_user(self, user: UsersSendDTO) -> bool:
        user_data = user.model_dump_json().encode()

        await self.__producer.start()
        try:
            result = await self.__producer.send_and_wait(
                settings.KAFKA_USERS_TOPIC,
                value=user_data,
            )
            return result is not None
        finally:
            await self.__producer.stop()

    @staticmethod
    async def send_public_key():
        producer = AIOKafkaProducer(
            bootstrap_servers=settings.KAFKA_BOOTSTRAP_SERVERS,
        )
        await producer.start()
        try:
            result = await producer.send_and_wait(
                settings.KAFKA_PUBLIC_KEY_TOPIC,
                value=settings.PUBLIC_KEY,
            )
            return result is not None
        finally:
            await producer.stop()
