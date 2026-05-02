from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm

from dependencies.token_version import TokenVersionServiceDep
from dependencies.user import UserServiceDep
from schemas.auth import LoginRequest
from schemas.token import FastAPIToken, TokenData, TokenResponse
from utils.token import create_auth_token

auth_router = APIRouter(prefix="/auth", tags=["Authentication"])

_certificate_error = HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Login failed")


@auth_router.post("/token", include_in_schema=False)
async def login_for_access_token(
    form_data: Annotated[OAuth2PasswordRequestForm, Depends()],
    user_service: UserServiceDep,
    token_version_service: TokenVersionServiceDep,
) -> FastAPIToken:
    user = await user_service.authenticate_user(email=form_data.username, password=form_data.password)
    if not user:
        raise _certificate_error
    token_version = await token_version_service.get_token_version(user_id=user.id)
    access_token_data = TokenData.access(user=user, token_version=token_version)
    return FastAPIToken(access_token=create_auth_token(access_token_data))


@auth_router.post("/login")
async def login_with_email_password(
    request: LoginRequest,
    user_service: UserServiceDep,
    token_version_service: TokenVersionServiceDep,
) -> TokenResponse:
    user = await user_service.authenticate_user(email=request.email, password=request.password)
    if not user:
        raise _certificate_error

    token_version = await token_version_service.get_token_version(user_id=user.id)
    access_token_data = TokenData.access(user=user, token_version=token_version)
    refresh_token_data = TokenData.refresh(user=user, token_version=token_version)
    return TokenResponse(access=create_auth_token(access_token_data), refresh=create_auth_token(refresh_token_data))
