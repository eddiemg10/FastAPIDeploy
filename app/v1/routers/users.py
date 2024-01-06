from fastapi import APIRouter, Depends, status, HTTPException
from app.core.database import get_database
from app.core.schemas import User
from app.core.repository import serialize
from app.core.repository.auth.hashing import Hash
from app.core.repository.auth import oauth2
from bson import ObjectId
from pymongo.errors import DuplicateKeyError
from app.core.repository.auth import users as UserController



# router = APIRouter(tags=["Users"], prefix="/users",dependencies=[Depends(oauth2.get_current_user)])
router = APIRouter(tags=["Users"], prefix="/users")


@router.get("", response_model=list[User.UserOut])
async def get_all_users(db = Depends(get_database)):
    return UserController.index(db=db)


@router.post("", response_model=User.UserOut)
async def create_user(request: User.UserIn, db = Depends(get_database)):
    return UserController.create(request=request, db=db)

@router.get("/{id}", response_model=User.UserOut)
async def get_single_user(id: str, db = Depends(get_database)):
    return UserController.show(id=id, db=db)

