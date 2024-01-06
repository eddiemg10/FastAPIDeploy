from app.core.schemas.ApiKey import ApiKeyIn, ApiKeyOut, ApiKey
from ..auth.hashing import Hash
from ...schemas.Project import Project, ProjectOut, APIKey
from ...database import get_database
from ..serialize import serializeDict, serializeList
from fastapi import Depends, status, HTTPException, Path
from bson import ObjectId
from pymongo.errors import DuplicateKeyError
from .. import helpers
import secrets
import datetime


def index(email, db):
    apikeys = db.apikeys.find({'user': email}, {'value': 0})
    return serializeList(apikeys)

def show(id, db):
    helpers.itemExists(id, db.apikeys, "API Key not found")
    apikey = db.apikeys.find_one({'_id': ObjectId(id)})
    return serializeDict(apikey)

def verify(key, db):
    return True

def create(request: ApiKeyIn, db, user):
    # Generate new API Key of 24 bytes long
    generated_key = secrets.token_urlsafe(24)
    display_key = f"{generated_key[:4]}{'*' * 26}{generated_key[30:]}"
    hashed_key = Hash.sha256(generated_key)
    key = {
        "value": hashed_key,
        "user": user['email'], 
        "description": request.description,
        "display": display_key,
        "active": True,
        "createdAt": datetime.datetime.now()
    }
    
    try:
        inserted_key =  db.apikeys.insert_one(key)
    except Exception:
        print(Exception)
        raise HTTPException(status_code=500, detail="Could not generate API Key")
    
    new_key_details = {
        "key": generated_key,
        "message": "This key will only be displayed once. Make sure you keep it safe"
    }
    return new_key_details

def update(id: str, request: ApiKey, db):
    helpers.verifyId(id)
    result = db.apikeys.update_one({"_id": ObjectId(id)}, {"$set": request.model_dump(exclude_unset=True)})
    if not result:
        raise HTTPException(status_code=404, detail="Api Key not found")
    return show(id, db)

def delete(id: str, db):
    helpers.verifyId(id)
    result = db.apikeys.delete_one({"_id": ObjectId(id)})
    if result.deleted_count == 0:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="API Key not found")
    return {"message": "API Key deleted successfully"}