from contextlib import asynccontextmanager
import asyncio

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from routers import user_profiles, images, profile_pictures, stacks
from config import settings
from logger import Logger
from database.database import create_tables
from synchronizer import Synchronizer
from database.models import UsersDB
from database.database import async_session_factory
from controllers import Users


@asynccontextmanager
async def lifespan(app: FastAPI):
    # Getting public key before start
    Logger.info("Receiving public key...")
    Logger.info(settings.DATABASE_URL)
    if await settings.get_public_key():
        Logger.info(f"Public key received")
    else:
        Logger.warning(f"Public key was not received")
    await create_tables()
    # Creating synchronizer and starting it
    synchronizer = Synchronizer(Users(UsersDB(async_session_factory)))
    synch_task = asyncio.create_task(synchronizer.start())
    yield
    synch_task.cancel()
    Logger.info(f"Auth-service ended")


app = FastAPI(lifespan=lifespan, root_path="profiles")

app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
app.include_router(user_profiles.router)
app.include_router(images.router)
app.include_router(profile_pictures.router)
app.include_router(stacks.router)
