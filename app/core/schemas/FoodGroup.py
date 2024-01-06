from bson import ObjectId
from pydantic import ConfigDict, BaseModel, Field

class FoodGroupBase(BaseModel):
    code: str = Field(description="Unique code identifying the food group", examples=["1"])
    name: str = Field(description="Name of the feed group", examples=["Cereals and cereal Products"])


class FoodGroupOut(FoodGroupBase):
    id: str = Field(..., alias="_id")
    model_config = ConfigDict(from_attributes=True)
    