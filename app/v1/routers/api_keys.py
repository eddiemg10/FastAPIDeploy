from fastapi import APIRouter, Depends, status, HTTPException, Path, Security
from fastapi.security import APIKeyHeader, APIKeyQuery
from app.core.database import get_database
from app.core.schemas import User
from app.core.schemas import ApiKey
from app.core.repository import serialize
from app.core.repository.auth.hashing import Hash
from app.core.repository.auth import oauth2
from bson import ObjectId
from pymongo.errors import DuplicateKeyError
from app.core.repository.auth import users as UserController
from app.core.repository.api_key import ApiKeyController



router = APIRouter(tags=["Api Keys"], prefix="/api-keys",dependencies=[Depends(oauth2.get_current_user)])


@router.get("", response_model=list[ApiKey.ApiKey])
async def get_api_keys(db = Depends(get_database), user=Depends(oauth2.get_current_user)):
    """
    Get all API Keys associated with user
    """
    return ApiKeyController.index(email=user['email'], db=db)


@router.post("", response_model=ApiKey.ApiKeyOut)
async def generate_api_key(request: ApiKey.ApiKeyIn, db = Depends(get_database), user=Depends(oauth2.get_current_user)):
    """
    Generat an API Key
    """
    return ApiKeyController.create(request=request, db=db, user=user)

@router.get("/{id}", response_model=ApiKey.ApiKey, deprecated=True)
async def get_single_api_key(id: str=Path(description="API key"), db = Depends(get_database)):
    return ApiKeyController.show(id=id, db=db)

@router.patch("/{id}")
async def update_api_key(request: ApiKey.ApiKeyUpdate, id: str=Path(description="ID of API Key to update"),  db = Depends(get_database)):
    return ApiKeyController.update(id, request=request, db=db)

@router.delete("/{id}")
async def update_api_key(id: str=Path(description="ID of API Key to delete"),  db = Depends(get_database)):
    return ApiKeyController.delete(id, db=db)
