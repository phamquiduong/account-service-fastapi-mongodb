from typing import Annotated

from fastapi import APIRouter, Depends
from fastapi.security import OAuth2PasswordRequestForm

from dependencies.user import UserMongoManagerDep
from helpers.auth import authenticate_user
from schemas.auth import LoginRequest
from schemas.token import FastAPIToken, TokenData, TokenResponse
from utils.token import create_auth_token

auth_router = APIRouter(prefix="/auth", tags=["Authentication"])


@auth_router.post("/token")
async def login_for_access_token(
    user_mongo_manager: UserMongoManagerDep, form_data: Annotated[OAuth2PasswordRequestForm, Depends()]
) -> FastAPIToken:
    user = await authenticate_user(user_mongo_manager, email=form_data.username, password=form_data.password)
    access_token_data = TokenData.access(user=user)
    return FastAPIToken(access_token=create_auth_token(access_token_data))


@auth_router.post("/login")
async def login_with_email_password(user_mongo_manager: UserMongoManagerDep, request: LoginRequest) -> TokenResponse:
    user = await authenticate_user(user_mongo_manager, email=request.email, password=request.password)
    access_token_data = TokenData.access(user=user)
    refresh_token_data = TokenData.refresh(user=user)
    return TokenResponse(access=create_auth_token(access_token_data), refresh=create_auth_token(refresh_token_data))
