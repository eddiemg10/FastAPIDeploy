from fastapi import APIRouter, Depends, status, HTTPException, Query
from app.core.database import get_database
from app.core.schemas.FoodGroup import FoodGroupOut
from app.core.repository import serialize
from app.core.repository.auth.hashing import Hash
from bson import ObjectId
from pymongo.errors import DuplicateKeyError
from app.core.repository.food import FoodGroupController



router = APIRouter(tags=["Food Groups"], prefix="/foodgroups")


@router.get("", response_model=list[FoodGroupOut])
async def get_foodgroups(db = Depends(get_database)):
    """
    Returns a list of food groups
    """
    return FoodGroupController.index(db=db)

# @router.get("", response_model=list[FoodGroupOut])
# async def get_foods_in_foodgroup(db = Depends(get_database),
#                     page: int = Query(1, description="Page number, starting from 1"),
#                     size: int = Query(10, description="Number of items per page")):
#     """
#     Returns a list of food items in the specified food group
#     """
#     return FoodGroupController.index(page=page, size=size , db=db)


# @router.post("", response_model=FoodGroupOut)
# async def add_food(request: FoodBase, db = Depends(get_database)):
#     """
#     Add a new food item
#     """
#     return FoodGroupController.create(request=request, db=db)


# @router.get("/random", response_model=FoodGroupOut)
# async def get_single_random_food(db = Depends(get_database)):
#     """
#     Get a random food item
#     """
#     return FoodGroupController.random(db=db)


# @router.get("/{id}", response_model=FoodGroupOut)
# async def get_single_food(id: str, db = Depends(get_database)):
#     """
#     Returns a food item with the specified id
#     """
#     return FoodGroupController.show(id=id, db=db)

# @router.put("/{id}")
# async def update_food(id: str, request: FoodUpdate, db = Depends(get_database)):
#     """
#     Updates a food item with the fields specified
#     """
#     return FoodGroupController.update(food_update=request, db=db, id=id)


# @router.delete("/{id}")
# async def delete_food(id: str, db = Depends(get_database)):
#     """
#     Deleted a food item by ID
#     """
#     return FoodGroupController.delete(db=db, id=id)



