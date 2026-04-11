from fastapi import APIRouter, HTTPException, status

from dependencies.auth import AuthUserDep
from dependencies.user import UserMongoManagerDep
from models.user import User
from schemas.user import AuthUserChangePasswordRequest
from utils.password import get_password_hash, verify_password

auth_user_router = APIRouter(prefix="/users/me", tags=["Authenticated user"])


@auth_user_router.get("")
async def get_authenticated_user_info(auth_user: AuthUserDep) -> User:
    return auth_user


@auth_user_router.post("/change_password", status_code=status.HTTP_204_NO_CONTENT)
async def change_authenticated_user_password(
    user_mongo_manager: UserMongoManagerDep, auth_user: AuthUserDep, request: AuthUserChangePasswordRequest
) -> None:
    if verify_password(plain_password=request.current_password, hashed_password=auth_user.password) is False:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Current password is incorrect")

    await user_mongo_manager.update_by_id(auth_user.id, {"password": get_password_hash(request.new_password)})
