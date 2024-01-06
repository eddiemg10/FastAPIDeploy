from typing import Optional
from bson import ObjectId
from pydantic import ConfigDict, BaseModel, Field


class UserBase(BaseModel):
    email: str = Field(..., examples=["john@example.com"])
    model_config = ConfigDict(from_attributes=True)

class UserIn(UserBase):
    password: str = Field(..., examples=["secret_password"])


class UserUpdate(UserBase):
    password: Optional[str] = Field(None, examples=["new_secret_password"])


class UserOut(UserBase):
    id: str = Field(..., alias="_id")


class User(UserBase):
    id: str = Field(..., alias="_id")
    model_config = ConfigDict(from_attributes=True)
