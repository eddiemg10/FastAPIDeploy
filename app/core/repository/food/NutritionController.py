from ...schemas import Food
from ...database import get_database
from ..serialize import serializeDict, serializeList
from fastapi import Depends, status, HTTPException
from bson import ObjectId
from pymongo.errors import DuplicateKeyError
from .. import helpers

def showNutrition(id, db):
    helpers.itemExists(id, db.foods, "Food item not found")
    pipeline = [
    {"$match": {"food_id": ObjectId(id)}},
    {"$lookup": {
        "from": "components",
        "localField": "component_id",
        "foreignField": "_id",
        "as": "component"
    }},
    {"$addFields": {
            "name": {"$arrayElemAt": ["$component.name", 0]},
            "unit": {"$arrayElemAt": ["$component.unit", 0]},
            "infoods_tagname": {"$arrayElemAt": ["$component.infoods_tagname", 0]},
            "denominator": {"$arrayElemAt": ["$component.denominator", 0]},
            "analysis_method" : {"$arrayElemAt": ["$component.analysis_method", 0]}
        }},

    {"$project": {
        "_id": 0,
        "name": 1,
        "unit": 1,
        "value": 1,
        "infoods_tagname": 1,
        "denominator": 1,
        "analysis_method" : 1


    }}
    ]
    results = serializeList(db.foodcomponentvalues.aggregate(pipeline))
    # db.foodcomponentvalues.aggregate(pipeline)
    # print(results)
    print("Done Processing")
    return results