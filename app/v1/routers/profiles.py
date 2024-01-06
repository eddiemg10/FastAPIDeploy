from fastapi import APIRouter, Depends, status, HTTPException, Path
from app.core.database import get_database
from app.core.schemas.Profile import ProfileOut, Profile
from app.core.repository.profiles import ProfileController


router = APIRouter(tags=["Profiles"], prefix="/profiles")

@router.get("", response_model=list[ProfileOut])
async def get_all_patient_profiles(db = Depends(get_database)):
    return ProfileController.index(db=db)


@router.post("", response_model=Profile)
async def create_patient_profile(request: Profile, db = Depends(get_database)):
    return ProfileController.create(request=request, db=db)

@router.get("/{id}", response_model=ProfileOut)
async def get_single_patient_profile(id: str =Path(description="ID of profile to fetch", example="6553a24b38657d30c74b9bfa"), db = Depends(get_database)):
    return ProfileController.show(id=id, db=db)

@router.patch("/{id}", response_model=ProfileOut)
async def update_patient_profile(request: Profile, id: str =Path(description="ID of profile to fetch"),  db = Depends(get_database)):
    return ProfileController.update(id, request=request, db=db)


@router.delete("/{id}")
async def delete_patient_profile(id: str =Path(description="ID of profile to delete"), db = Depends(get_database)):
    return ProfileController.delete(id=id, db=db)
