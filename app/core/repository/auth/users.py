from ...schemas import User
from ...database import get_database
from .hashing import Hash
from ..serialize import serializeDict, serializeList
from fastapi import Depends, status, HTTPException
from bson import ObjectId
from pymongo.errors import DuplicateKeyError



def index(db ):
    users = db.users.find()
    return serializeList(users)

def show(id : str, db):
    user =  db.users.find_one({"_id": ObjectId(id)})
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="User not found"
        )
    return serializeDict(user)


def create(request: User.UserIn, db):
    if db.users.find_one({"email": request.email}):
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="An account with this email already exists")
    hashed_password = Hash.encrypt(request.password)
    print(request.password, hashed_password)
    user = {
            "email": request.email,
            "password": hashed_password,
        }
    try:
        inserted_user =  db.users.insert_one(user)
    except DuplicateKeyError:
        raise HTTPException(status_code=400, detail="Email already registered")
    return serializeDict(db.users.find_one({"_id" : inserted_user.inserted_id}))