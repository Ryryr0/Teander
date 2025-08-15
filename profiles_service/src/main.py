from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from routers import user_profiles, images, profile_pictures, stacks
from config import settings


@asynccontextmanager
async def lifespan(app: FastAPI):
    # Getting public key before start 
    await settings.get_public_key()
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
