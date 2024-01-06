from fastapi import APIRouter, Query, Security
from app.core.database import get_database
from app.core.repository.healthmetrics import amdr, bmi, eer, pal, blood_sugar
from app.core.schemas.HealthMetrics import EEROut, EERIn, BmiOut, BmiIn, PAL, PALIn, PALOut, BloodSugarUnits, BloodSugarIn, BloodSugarOut
from app.core.repository.auth import apikey


router = APIRouter(tags=["Health metrics"], prefix="/healthmetrics")

@router.post("/bmi",response_model=BmiOut)
async def calculate_bmi(request: BmiIn):
    """
    Calculates the bmi given an individuals height and weight
    """
    return bmi.calculate_bmi(request)

@router.get("/pal", response_model=list[PAL])
async def get_physical_activity_level_activities(api_key: str = Security(apikey.get_api_key)):
    return pal.retrieve_pal_activites()

@router.post("/pal", response_model=PALOut)
async def determine_physical_activity_level(request: list[PALIn], api_key: str = Security(apikey.get_api_key)):
    return pal.calculate_pal(request)

@router.post("/eer", response_model=EEROut)
async def calculate_estimated_energy_requirements(request: EERIn, api_key: str = Security(apikey.get_api_key)):
    """
    Claculates the estimated energy requirements of an individual based on parameters x
    """
    return eer.calculate_eer(request)

@router.get("/amdr")
async def acceptable_macronutrient_distribution_range(api_key: str = Security(apikey.get_api_key)):
    """
    Calculates the acceptable_macronutrient_distribution_range
    """
    return "Hello"

# @router.get("/bloodsugar")
# async def bloog_sugar_levels():
#     """
#     Converts and interprets blood sugar levels from different types of tests
#     """
#     return "Hello"

@router.post("/bloodsugar", response_model=BloodSugarOut)
async def bloog_sugar_levels(request: BloodSugarIn, api_key: str = Security(apikey.get_api_key)):
    """
    Converts and interprets blood sugar levels from different types of tests
    """
    return blood_sugar.interpret_blood_sugar(request)
