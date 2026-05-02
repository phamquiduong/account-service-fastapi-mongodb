from typing import Annotated

from fastapi import Depends

from dependencies.mongodb.token_version import TokenVersionMongoManagerDep
from services.token_version import TokenVersionService


def _get_token_version_service(token_version_mongo_manager: TokenVersionMongoManagerDep) -> TokenVersionService:
    return TokenVersionService(token_version_mongo_manager=token_version_mongo_manager)


TokenVersionServiceDep = Annotated[TokenVersionService, Depends(_get_token_version_service)]
