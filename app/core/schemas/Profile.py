from datetime import datetime
from typing import Optional
from bson import ObjectId
from pydantic import ConfigDict, BaseModel, Field
from .HealthMetrics import PALType, BloodSugar, BloodSugarIn, Gender, PALOut

class BloodSugarEntry(BloodSugarIn):
    date: datetime

class Profile(BaseModel):
    height: float = Field(None, description="Height of patient in cm", example=180)
    weight: int = Field(None, description="Weight of patient in kg", example=65)
    age: int = Field(None, description="Age of the patient", example=19)
    gender: Gender = Field(None, description="Gender of the patient", example=19)
    location: str = Field(None, description="General Location Area of user", example="coast")
    pal: PALType = Field(None, description="Physical Activity Level", example="inactive")
    eer: float = Field(None, description="Estimated Energy requirement value", example = 2500.6)
    HbA1C: BloodSugar = Field(None, description="Average blood sugar (glucose) over the past two to three months.")
    blood_sugar_history: list[BloodSugarEntry] = Field(None, description="History of patient's recorded blood sugar levels")
    cuisine: list[str] = Field(None, description="Preferred cuisines", example=["Indian"])
    exclude: list[str] = Field(None, description="Foods to exclude", example=["meat"])

class ProfileOut(Profile):
    id: str = Field(..., alias="_id")


class ProfileUpdate(Profile):
    password: Optional[str] = Field(None, examples=["new_secret_password"])


class RecommendationProfile(BaseModel):
    height: float = Field(None, description="Height of patient in cm", example=180)
    weight: int = Field(None, description="Weight of patient in kg", example=65)
    age: int = Field(None, description="Age of the patient", example=19)
    gender: Gender = Field(None, description="Gender of the patient", example="male")
    location: str = Field(None, description="General Location Area of user", example="coast")
    pal: PALOut = Field(None, description="Physical Activity Level", example={"pal":"active", "value": 2.43})
    coords: list[float] = Field(None, description="Long | Lat coordinates", example=[39, -3])
    HbA1C: BloodSugar = Field(None, description="Average blood sugar (glucose) over the past two to three months.")
    blood_sugar_history: list[BloodSugarEntry] = Field(None, description="History of patient's recorded blood sugar levels")
    exclude: list[str] = Field(None, description="Foods to exclude", example=["meat"])