from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from config import settings
from routers import users

from database.queries import create_tables

import asyncio
from routers.users import registrate_user
from schemas import UserPostDTO


app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
app.include_router(users.router)


@app.on_event("startup")
def on_startup():
    create_tables()

# asyncio.run(registrate_user(UserPostDTO(username="Art", email="art@gmail.com"), password='123'))
