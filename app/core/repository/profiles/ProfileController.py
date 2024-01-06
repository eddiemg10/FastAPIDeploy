from ...schemas.Profile import Profile, ProfileOut, ProfileUpdate
from ...database import get_database
from ..serialize import serializeDict, serializeList
from fastapi import Depends, status, HTTPException, Path
from bson import ObjectId
from pymongo.errors import DuplicateKeyError
from .. import helpers



def index(db ):
    profiles = db.profiles.find()
    return serializeList(profiles)

def show(id : str, db):
    helpers.verifyId(id)
    profile =  db.profiles.find_one({"_id": ObjectId(id)})
    if not profile:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Profile not found"
        )
    return serializeDict(profile)


def create(request: Profile, db):
    hst = []
    for reading in request.blood_sugar_history:
        hst.append(dict(reading))
        
    profile = {
            "height": request.height,
            "weight": request.weight,   
            "age": request.age,   
            "location": request.location,
            "pal": request.pal,   
            "eer": request.eer,   
            "HbA1C": dict(request.HbA1C),   
            "blood_sugar_history": [dict(hst) for hst in request.blood_sugar_history],   
            "cuisine": request.cuisine,   
            "exclude": request.exclude,   
        }
    try:
        inserted_profile =  db.profiles.insert_one(profile)
    except Exception:
        print(Exception)
        raise HTTPException(status_code=500, detail="Could not create profile")
    return serializeDict(db.profiles.find_one({"_id" : inserted_profile.inserted_id}))

def update(id: str, request: Profile, db):
    helpers.verifyId(id)
    result = db.profiles.update_one({"_id": ObjectId(id)}, {"$set": request.model_dump(exclude_unset=True)})
    if not result:
        raise HTTPException(status_code=404, detail="Patient profile not found")
    # updated_profile = db.foods.find_one({"_id": ObjectId(id)})
    return show(id, db)

def delete(id: str, db):
    helpers.verifyId(id)
    result = db.profiles.delete_one({"_id": ObjectId(id)})
    if result.deleted_count == 0:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Patient profile not found")
    return {"message": "Patient profile deleted successfully"}

