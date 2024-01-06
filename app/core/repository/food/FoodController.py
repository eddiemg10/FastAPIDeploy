from ...schemas import Food
from ...database import get_database
from ..serialize import serializeDict, serializeList
from .. import helpers
from fastapi import Depends, status, HTTPException
from bson import ObjectId
from pymongo.errors import DuplicateKeyError
from random import randint
from app.core.repository.expertipy.engine import FoodGroups
import csv 


def noGI(db):
    foods = db.foods.find({ "GI": { "$exists": False } })
    # return len(serializeList(foods))
    return serializeList(foods)


def index(page, size, db, groups):
    skip = (page - 1) * size
    if groups:
        group_objectids = []
        for group_id in groups:
            try:
                group_objectids.append(ObjectId(group_id))
            except:
                raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail="Invalid Food Group Id given"
        )
        foods = db.foods.find({'foodgroup_id': {'$in': group_objectids}}).skip(skip).limit(size)
    else:
        foods = db.foods.find().skip(skip).limit(size)


    return serializeList(foods)

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

def filter(db, query, sort_by="GI"):
    FG = FoodGroups()
    # Define the base query
    base_query = {}

    # Check if "GI" filter is provided
    if "GI" in query:
        min_gi, max_gi = query["GI"]
        base_query["GI"] = {"$gte": min_gi, "$lte": max_gi}

    # Check other filters
    if "location" in query:
        location_value = query["location"]
        if location_value:
            location_query = {"location": {"$regex": f'{location_value}|{location_value},|,{location_value}$|^ {location_value},|, {location_value},|, {location_value}$'}}
            base_query.update(location_query)
    
    if "cuisine" in query:
        location_value = query["cuisine"]
        if location_value:
            location_query = {"location": {"$regex": f'{location_value},{location_value},|,{location_value}$|^ {location_value},|, {location_value},|, {location_value}$'}}
            base_query.update(location_query)

    if "group" in query:
        # groups = []
        # # for grp in query["group"]:
        # #     groups.append(grp)
        # base_query["foodgroup_id"] = {"$in": [ObjectId(query["group"])]}
        groups = query["group"]
        base_query["foodgroup_id"] = {"$in": [ObjectId(group) for group in groups]}

    if "tags" in query:
        tags_value = query["tags"]
        if tags_value == "":
            # If tags is an empty string, retrieve foods where the tag field is empty
            base_query["$or"] = [{"tag": {"$exists": False}}, {"tag": ""}]
        else:
            # Otherwise, perform the regex query
            tags_query = {"tag": {"$regex": f'{tags_value}|{tags_value},|,{tags_value}$|^ {tags_value},|, {tags_value},|, {tags_value}$'}}
            base_query.update(tags_query)

    if "exclude" in query:
        exclude_options = {"meat": FG.meats_and_poultry, "fish": FG.fish, "dairy": FG.dairy}  # Map exclude options to group_ids
        exclude_values = query["exclude"]
        exclude_group_ids = [exclude_options.get(exclude_value) for exclude_value in exclude_values if exclude_options.get(exclude_value)]
        if exclude_group_ids:
            base_query["foodgroup_id"] = {"$nin": [ObjectId(group_id) for group_id in exclude_group_ids]}

    # Sort by the specified field (default: "GI")
    sort_field = sort_by if sort_by in ["GI", "location", "group", "tags"] else "GI"
    cursor = db.foods.find(base_query).sort(sort_field)

    group_map = {
        "653e83a8fe351cbe412097ed" : "Cereals and cereal products",
        "653e83aafe351cbe412097f0" : "Starchy roots, bananas and tubers",
        "653e83aafe351cbe412097f3" : "Legumes and pulses",
        "653e83aafe351cbe412097f6" : "Vegetables and vegetable products",
        "653e83abfe351cbe412097f9" : "Fruits and fruit products",
        "653e83abfe351cbe412097fb" : "Milk and dairy products",
        "653e83abfe351cbe412097fd" : "Meats, poultry and eggs",
        "653e83abfe351cbe412097ff" : "Fish and sea foods",
        "653e83acfe351cbe41209801" : "Oils and fats",
        "653e83acfe351cbe41209803" : "Nuts and seeds",
        "653e83acfe351cbe41209805" : "Sugar and sweetened products",
        "653e83acfe351cbe41209807" : "Beverages",
        "653e83adfe351cbe41209809" : "Condiments and spices",
        "653e83adfe351cbe4120980b" : "Insects",
        "653e83adfe351cbe4120980d" : "Mixed dishes",
    }
    grouped_results = {}
    for food in serializeList(cursor):
        group_id = str(food.get("foodgroup_id", ""))
        group_name = group_map[group_id]
        if group_name not in grouped_results:
            grouped_results[group_map[group_id]] = []
        grouped_results[group_map[group_id]].append(food)

    # for group_id, foods in grouped_results.items():
    #     grouped_results[group_id] = sorted(foods, key=lambda x: x.get("GI", 0))
    return grouped_results
    return serializeDict(grouped_results)
    # Perform the query
    result = serializeList(cursor)
    # result = serializeList(db.foods.find(base_query))

    return result


def updateLocations(db):    
    updates = []
    with open('output.csv', 'r') as csv_file:
        csv_reader = csv.DictReader(csv_file)
        # Iterate through each row in the CSV
        for row in csv_reader:
            index_field = row['index']
            location_field = row['location']

            # Check if the location field is not blank
            if location_field.strip():
                # Query MongoDB to find the document where kfct field is equal to the index field
                result = db.foods.find_one({'code_kfct': index_field})

                # If a document is found, display the id along with index and location fields
                if result:
                    id = result['_id']
                    print(f"ID: {result['_id']}, Index: {index_field}, Location: {location_field}")
                    update = serializeDict({
                        "location": location_field
                    })
                    updated_result = db.foods.update_one(
                    {"_id": ObjectId(id)},
                    {"$set": {"location": location_field}}
                    )
                    print(db.foods.find_one({'code_kfct': index_field}))

                
    print(updates)
    return "done"