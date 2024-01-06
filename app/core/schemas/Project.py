from typing import Optional
from bson import ObjectId
from pydantic import ConfigDict, BaseModel, Field


class Project(BaseModel):
    name: str = Field(description="Name given to the project related to the API Key", examples=["My simple project"])
    user_id: str = Field(description="Reference to the group the food belongs in", examples=["6564f31b1fb28355968d09b7"])

class ProjectOut(Project):
    id: str = Field(description="Unique identifier of the project", alias="_id")


class APIKey(BaseModel):
    key: str = Field(description="Value of the API Key. This is only showed once")
    description: str = Field(description="Desciption of the Key")
    active: bool = Field(description="Status of the API Key")


class APIKey(BaseModel):
    id: str = Field(description="Unique identifier of the Key", alias="_id")
    preview: str = Field(description="Preview of the Key", alias="_id")
