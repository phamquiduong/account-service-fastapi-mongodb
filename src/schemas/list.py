from typing import Annotated

from fastapi import Depends
from pydantic import BaseModel, Field


class ListQuery(BaseModel):
    skip: int = Field(default=0, ge=0)
    limit: int = Field(default=100, ge=1, le=100)


ListQueryDep = Annotated[ListQuery, Depends()]
