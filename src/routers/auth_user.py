from fastapi import APIRouter, HTTPException, status

from dependencies.auth import AuthUserDep
from dependencies.services.user import UserServiceDep
from models.user import User
from schemas.user import AuthUserChangePasswordRequest
from utils.password import verify_password

auth_user_router = APIRouter(prefix="/users/me", tags=["Authenticated user"])


@auth_user_router.get("")
def get_authenticated_user_info(auth_user: AuthUserDep) -> User:
    return auth_user


@auth_user_router.post("/change_password", status_code=status.HTTP_204_NO_CONTENT)
async def change_authenticated_user_password(
    user_service: UserServiceDep, auth_user: AuthUserDep, request: AuthUserChangePasswordRequest
) -> None:
    if verify_password(plain_password=request.current_password, hashed_password=auth_user.password) is False:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Current password is incorrect")

    await user_service.update_password(user_id=auth_user.id, new_password=request.new_password)
