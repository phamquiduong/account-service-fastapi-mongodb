import logging

from fastapi import APIRouter, Body, HTTPException, status
from pydantic import EmailStr

from dependencies.user import UserMongoManagerDep
from schemas.token import TokenData, TokenResponse
from utils.password import verify_password
from utils.token import create_auth_token

logger = logging.getLogger(__name__)

auth_router = APIRouter(prefix="/auth", tags=["Authentication"])


@auth_router.post("/login")
async def login_with_email_password(
    user_mongo_manager: UserMongoManagerDep, email: EmailStr = Body(), password: str = Body()
) -> TokenResponse:
    certificate_error = HTTPException(status_code=status.HTTP_400_BAD_REQUEST)

    user = await user_mongo_manager.get(query={"email": email})
    if user is None:
        logger.warning("user with email [%s] does not exist", email)
        raise certificate_error

    if verify_password(plain_password=password, hashed_password=user.password) is False:
        logger.warning("user with email [%s] wrong password", email)
        raise certificate_error

    access_token_data = TokenData.access(user=user)
    refresh_token_data = TokenData.refresh(user=user)
    return TokenResponse(access=create_auth_token(access_token_data), refresh=create_auth_token(refresh_token_data))
