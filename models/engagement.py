from typing import Optional
from uuid import UUID

from pydantic import Field

from models.basic import TimeStamp


class Bookmark(TimeStamp):
    user_uid: UUID = Field(..., description="User ID")
    film_uid: UUID = Field(..., description="Film ID")


class Like(TimeStamp):
    user_uid: UUID = Field(..., description="User ID")


class Review(TimeStamp):
    user_uid: UUID = Field(..., description="User ID")
    film_uid: UUID = Field(..., description="Film ID")
    rating: int = Field(..., gt=0, lt=10, description="Review rating")
    description: Optional[str] = Field(default=None, description="Review description")
