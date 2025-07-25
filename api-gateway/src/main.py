import httpx
import uvicorn

from fastapi import FastAPI, Request, Depends, HTTPException
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware

from config import settings
from routers import auth


app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
app.include_router(auth.router)


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8080)
