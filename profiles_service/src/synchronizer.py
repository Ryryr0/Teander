import json
import asyncio

from aiokafka import AIOKafkaConsumer

from config import settings
from interfaces import ISynchronizer, IUsers
from logger import Logger
from schemas import UsersDTO, UsersPostDTO


class Synchronizer(ISynchronizer):
    def __init__(self, users: IUsers):
        self.consumer = None
        self.users = users

    async def start(self):
        self.consumer = AIOKafkaConsumer(
            settings.KAFKA_USERS_TOPIC,
            bootstrap_servers=settings.KAFKA_BOOTSTRAP_SERVERS,
            group_id=settings.KAFKA_GROUP,
        )

        await self.consumer.start()
        try:
            async for msg in self.consumer:
                Logger.info(f"User received from kafka topic: {settings.KAFKA_USERS_TOPIC}")
                if not isinstance(msg.value, bytes):
                    Logger.warning(f"Unknown values received from kafka")
                    continue
                msg = json.loads(msg.value.decode())
                user = UsersDTO(**msg["user_data"])
                if msg["operation"] == "create":
                    if not await self.users.create_user(user.id, UsersPostDTO(**user.model_dump())):
                        Logger.warning(f"User, received from kafka topic: {settings.KAFKA_USERS_TOPIC}, not created")
                elif msg["operation"] == "update":
                    if not await self.users.update_user(user.id, UsersPostDTO(**user.model_dump()), allow_main_data_changes=True):
                        Logger.warning(f"User, received from kafka topic: {settings.KAFKA_USERS_TOPIC}, not updated")
                elif msg["operation"] == "delete":
                    if not await self.users.delete_user(user.id):
                        Logger.warning(f"User, received from kafka topic: {settings.KAFKA_USERS_TOPIC}, not deleted")
        except asyncio.CancelledError:
            Logger.info(f"Kafka synchronizer consumer cancelled")
        finally:
            await self.consumer.stop()
            