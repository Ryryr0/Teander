import uvicorn
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from config import settings
from routers import users

from database.database import create_tables

from fastapi.testclient import TestClient


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
async def on_startup():
    await create_tables()

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
