from fastapi import APIRouter, Depends, status, Query, Header
from app.core.database import get_database
from app.core.repository.locations import LocationController
from pydantic import ConfigDict, BaseModel, Field
from enum import Enum


router = APIRouter(tags=["Locations"], prefix="/locations")

class HeaderValue(Enum):
    application_json = "application/json"
    image_png = "image/png"

@router.get("")
async def get_all_counties(expect_response:HeaderValue = Header(description="Content to be sent back by server from the request.", default=HeaderValue.application_json), db = Depends(get_database), lat: float | None = Query(description="Latitude in degrees", default=None), long: float | None = Query(description="Longitude in degrees", default=None)):
    
    if lat and long:
        coords = (long, lat)
        return LocationController.find_county_and_highlight(coordinate=coords, image_flag=expect_response == HeaderValue.image_png)
    else:
        if expect_response == HeaderValue.application_json:
            return LocationController.get_all_counties()
        elif expect_response == HeaderValue.image_png:
            return LocationController.get_all_counties(image_flag=True)
    


# @router.get("")
# async def get_all_counties(db = Depends(get_database)):
#     return LocationController.get_all_counties()

