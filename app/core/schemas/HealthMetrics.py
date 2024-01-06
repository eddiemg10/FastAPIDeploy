from typing import Annotated
from pydantic import ConfigDict, BaseModel, Field, validator
from enum import Enum

class Gender(str, Enum):
    male = "male"
    female = "female"

class GlucoseTest(str, Enum):
    A1C = "A1C"
    random = "random"
    fasting = "fasting"
    tolerance = "tolerance"

class BloodSugarUnits(str, Enum):
    mg_dL = "mg/dL",
    mmol_L = "mmol/L",
    percentage = "%"

class PALType(str, Enum):
    inactive = "inactive"
    low_active = "low active"
    active = "active"
    very_active = "very active"

class EERIn(BaseModel):
    age: int = Field(description="Age in years", example=18)
    height: float = Field(description="Height in cm", example=180.4)
    weight: float = Field(description="Weight in Kg", example = 70)
    gender: Gender = Field(description="Male or Female", example = "male")
    pal: PALType = Field(description="Physical Activity Level", example = "very active")

class EEROut(BaseModel):
    value: float = Field(description="Estimated Energy requirement value", example = 2500.6)
    description: str = Field("kcal/ day", description="Units of the value", example = "kcal/day")

class BmiIn(BaseModel):
    height: float = Field(description="Height in cm", example=180.4)
    weight: float = Field(description="Weight in Kg", example = 70)

class BmiOut(BaseModel):
    bmi: float = Field(description="Calculated BMI", example=21.509)

class PAL(BaseModel):
    activity: str  = Field(description="Description of the activity", example="Driving")
    par: float = Field(description="Energy costs of activities, expressed as multiples of basal metabolic rate", example=2.0)

class PALIn(PAL):
    time: float = Field(description="Amount of time spent doing activity in hours", example=3)

class PALOut(BaseModel):
    pal: PALType = Field(description="Physical Activity Level", example="very active")
    value: float = Field(description="PAL value", example=2.5041)

class BloodSugar(BaseModel):
    value: float = Field(description="Value of blood sugar readings", example=120)
    units: BloodSugarUnits = Field(description="Units of the blood sugar value: mg/dL or mmol/l", example="mg/dL")

class BloodSugarIn(BloodSugar):
    test: GlucoseTest = Field(description="Type of blood sugar test", example="random") 

class BloodSugarOut(BaseModel):
    blood_sugar_level: list[BloodSugar] = Field(description="Original value of blood sugar readings converted into both formats")
    test: GlucoseTest = Field(description="Type of blood sugar test", example="random")
    level: str = Field(description="Interpretation of the readings")



# [
#   {
#     "activity": "Sleeping",
#     "par": 1,
#     "time": 6
#   },
#   {
#     "activity": "Personal care (dressing, bathing)",
#     "par": 2.3,
#     "time": 1
#   },
#   {
#     "activity": "Eating",
#     "par": 1.4,
#     "time": 1
#   },

#   {
#     "activity": "Cooking",
#     "par": 2.1,
#     "time": 1
#   },
#   {
#     "activity": "Non-mechanized agricultural work",
#     "par": 4.1,
#     "time": 8
#   },
# {
#     "activity": "Collecting water/wood",
#     "par": 4.4,
#     "time": 1
#   },
# {
#     "activity": "Non-mechanized domestic chores",
#     "par": 2.3,
#     "time": 1
#   },
# {
#     "activity": "Walking at varying paces without a laod",
#     "par": 3.2,
#     "time": 1
#   },
#   {
#     "activity": "Light Leisure Activities",
#     "par": 1.4,
#     "time": 4
#   }
# ]