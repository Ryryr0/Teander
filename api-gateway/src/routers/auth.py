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
    prefix="/auth",
    tags=["auth"],
    responses={404: {"description": "Auth not found"}},
)


@router.post("/token")
async def get_access_token(
        form_data: Annotated[OAuth2PasswordRequestForm, Depends()],
):
    data = {
        key: getattr(form_data, key)
        for key in ["username", "password", "scopes", "client_id", "client_secret"]
    }
    async with httpx.AsyncClient() as client:
        request_id: int = Logger.log_request(f"Request from user<username: {form_data.username}> to {URLS.auth_token_url}")
        response = await client.post(URLS.auth_token_url, data=data)
        if response:
            Logger.log_request(
                f"Response received for user<username: {form_data.username}> from {URLS.auth_token_url}",
                request_id,
            )
        if "application/json" in response.headers.get("content-type", ""):
            return JSONResponse(content=response.json(), status_code=response.status_code)
        else:
            return Response(content=response.text, status_code=response.status_code)


@router.post("/reg")
async def registrate(
        form_data: Annotated[UserPostDTO, Depends(get_user_post_form)],
        password: Annotated[str, Form()],
):
    data = form_data.dict()
    data.update(password=password)

    async with httpx.AsyncClient() as client:
        request_id: int = Logger.log_request(f"Request from user<username: {form_data.username}> to {URLS.auth_reg_url}")
        response = await client.post(URLS.auth_reg_url, data=data)
        if response:
            Logger.log_request(
                f"Response received for user<username: {form_data.username}> from {URLS.auth_reg_url}",
                request_id,
            )
        if "application/json" in response.headers.get("content-type", ""):
            return JSONResponse(content=response.json(), status_code=response.status_code)
        else:
            return Response(content=response.text, status_code=response.status_code)


@router.put("update-user")
async def update_user(
        token: Annotated[str, Depends(get_token)],
        token_data: Annotated[TokenData, Depends(get_token_data)],
        new_user_data: Annotated[UserPostDTO, Depends(get_user_post_form)],
):
    async with httpx.AsyncClient() as client:
        request_id: int = Logger.log_request(f"Request from user<id: {token_data.id}> to {URLS.auth_update_user_url}")
        response = await client.put(
            URLS.auth_update_user_url,
            data=new_user_data.dict(),
            headers={"Authorization": f"Bearer {token}"},
        )
        if response:
            Logger.log_request(
                f"Response received for user<id: {token_data.id}> from {URLS.auth_update_user_url}",
                request_id,
            )
        if "application/json" in response.headers.get("content-type", ""):
            return JSONResponse(content=response.json(), status_code=response.status_code)
        else:
            return Response(content=response.text, status_code=response.status_code)


@router.delete("/delete")
async def delete_user(
        token: Annotated[str, Depends(get_token)],
        token_data: Annotated[TokenData, Depends(get_token_data)],
):
    async with httpx.AsyncClient() as client:
        request_id: int = Logger.log_request(f"Request from user<id: {token_data.id}> to {URLS.auth_delete_user_url}")
        response = await client.delete(URLS.auth_delete_user_url, headers={"Authorization": f"Bearer {token}"})
        if response:
            Logger.log_request(
                f"Response received for user<id: {token_data.id}> from {URLS.auth_delete_user_url}",
                request_id,
            )
        if "application/json" in response.headers.get("content-type", ""):
            return JSONResponse(content=response.json(), status_code=response.status_code)
        else:
            return Response(content=response.text, status_code=response.status_code)
