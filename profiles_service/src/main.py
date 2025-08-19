from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from routers import user_profiles, images, profile_pictures, stacks
from config import settings
from logger import Logger
from database.database import create_tables


@asynccontextmanager
async def lifespan(app: FastAPI):
    # Getting public key before start
    if await settings.get_public_key():
        Logger.info(f"Public key received")
    else:
        Logger.warning(f"Public key was not received")
    await create_tables()
    yield


app = FastAPI(lifespan=lifespan)
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
