from fastapi import status, HTTPException
from bson import ObjectId, errors

def verifyId(id):
    try:
        ObjectId(id)
    except errors.InvalidId:
        raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST, detail="Invalid ObjectId, it must be a 12-byte input or a be a 12-byte input or a 24-character hex string"
            )

def itemExists(id, collection, response):
    verifyId(id)
    if not collection.find_one({"_id": ObjectId(id)}):
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, detail=response
            )

def checkDuplicate(id, collection, response):
    verifyId(id)
    if collection.find_one({"_id": ObjectId(id)}):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST, detail=response
            )