from ...schemas import Food
from ...database import get_database
from ..serialize import serializeDict, serializeList
from fastapi import Depends, status, HTTPException
from bson import ObjectId, errors
from pymongo.errors import DuplicateKeyError
from random import randint
from .. import helpers

def index(db):
    groups = db.foodgroups.find()
    return serializeList(groups)

def show(id, db):
    helpers.itemExists(id, db.foods, "Food item not found")
    food =  db.foods.find_one({"_id": ObjectId(id)})

    return serializeDict(food)

def create(request: Food.BaseModel, db):
    if db.foods.find_one({"code_kfct": request.code_kfct}):
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="A food with a similar KFCT code already exists")
    food = {
            "code_kfct": request.code_kfct,
            "code_ken": request.code_ken,
            "english_name": request.english_name,
            "scientific_name": request.scientific_name,
            "foodgroup_id": ObjectId(request.foodgroup_id),
            "biblio_id": request.biblio_id,
        }
    try:
        inserted_food =  db.foods.insert_one(food)
    except DuplicateKeyError:
        raise HTTPException(status_code=400, detail="Food already exists")
    return serializeDict(db.foods.find_one({"_id" : inserted_food.inserted_id}))


def update(id, food_update, db):
    food =  db.foods.find_one({"_id": ObjectId(id)})
    if not food:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Food not found"
        )
    
    result = db.foods.update_one({"_id": ObjectId(id)}, {"$set": food_update.dict(exclude_unset=True)})
    if not result:
        raise HTTPException(status_code=404, detail="Food item not found")
    updated_food = db.foods.find_one({"_id": ObjectId(id)})
    return serializeDict(updated_food)

def delete(id, db):
    result = db.foods.delete_one({"_id": ObjectId(id)})
    if result.deleted_count == 0:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Food item not found")
    return {"message": "Food item deleted successfully"}

def random(db):
    count = 582
    random_index = randint(0, count - 1)
    random_food = db.foods.find_one(skip=random_index)
    if random_food is None:
        raise HTTPException(status_code=404, detail="No food items found")
    return serializeDict(random_food)