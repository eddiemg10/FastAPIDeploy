from fastapi import APIRouter, Query
from app.core.repository.expertipy import engine
from app.core.schemas.Profile import RecommendationProfile

router = APIRouter(tags=["Recommendations"], prefix="/recommendations")

@router.get("/test")
async def get_recommendation():
    return engine.recommend()

@router.post("")
async def generate_recommendation(request: RecommendationProfile):
#     req = {
#     "height": 180,
#     "weight": 65,
#     "bmi": 23, 
#     "age": 20,
#     "gender": "male",
#     "coords": (39,-3),
#     "pal": {"pal":"active", "value": 2.43},
#     "eer": 2500.6,
#     "HbA1C": None,
#     "blood_sugar_history": [
#       {
#         "value": 69,
#         "units": "mg/dL",
#         "test": "fasting",
#         "date": "2023-11-18T16:27:36.309Z"
#       }
#     ],
#     "exclude": ["fish"],
#     "_id": "string",
#   }
    return engine.recommend(request)
