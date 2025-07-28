from typing import Annotated
import httpx

from fastapi.routing import APIRouter
from fastapi import Depends, status, Form
from fastapi.responses import JSONResponse, Response
from fastapi.security import OAuth2PasswordRequestForm

from config import URLS
from schemas import TokenData, UserPostDTO
from logger import Logger
from dependencies import get_token, get_token_data, get_user_post_form


router = APIRouter(
    prefix="/profiles",
    tags=["profiles"],
    responses={404: {"description": "Auth not found"}},
)


@router.post("/create-profile")
async def create_profile():
    pass


@router.post("/add-photo")
async def add_photo():
    pass
