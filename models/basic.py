from datetime import datetime
from uuid import UUID

from bson import ObjectId
from pydantic import BaseModel, ConfigDict, Field


class PyObjectId(ObjectId):
    @classmethod
    def __get_validators__(cls):
        yield cls.validate

    @classmethod
    def validate(cls, v):
        if not ObjectId.is_valid(v):
            raise ValueError("Invalid object id.")
        return ObjectId(v)


class TimeStamp(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: UUID | None = Field(default=None, description="Document ID")
    created: datetime | None = Field(
        default_factory=datetime.now, description="Document creation time"
    )
    modified: datetime | None = Field(
        default_factory=datetime.now, description="Document modification time"
    )

    def touch(self):
        self.modified = datetime.now()
