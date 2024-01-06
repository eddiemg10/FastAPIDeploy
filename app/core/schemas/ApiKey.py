from datetime import datetime
from typing import Optional
from bson import ObjectId
from pydantic import ConfigDict, BaseModel, Field
import datetime

class ApiKey(BaseModel):
    value: str = Field(None, description="Hashed value of the API Key", example="XXXX_XXX")
    user: str = Field(None, description="Email of who owns the Key", example="john@example.com")
    description: str = Field(None, description="Description of what the key is for", example="API Key for the NourishKe App")
    display: str = Field(None, description="Display value of key", example="qsW-OO**********o8")
    active: bool = Field(description="Status of the API Key")
    createdAt: datetime.datetime = Field(None, description="Time the Key was generated", example="2023-12-22T20:35:31.407+00:00")

class ApiKeyIn(BaseModel):
    description: str = Field(None, description="Description of what the API Key is for", example="API Key for the NourishKe App")

class ApiKeyOut(BaseModel):
    key: str = Field(None, description="Value of the API Key, only displayed once", example="okOcQ2tMeLE5bTCW3-qP3feTjgYy6s8M")
    message: str = Field("This key will only be displayed once. Make sure you keep it safe", description="Message", example="This key will only be displayed once. Make sure you keep it safe")

class ApiKeyUpdate(BaseModel):
    description: str = Field(None, description="Description of what the key is for", example="API Key for the NourishKe App") 
    active: bool = Field(description="Status of the API Key") 
