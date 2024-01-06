from fastapi import APIRouter, Depends, status, HTTPException
from fastapi.security import OAuth2PasswordRequestForm
from app.core.repository.auth.hashing import Hash
from app.core.repository.auth import JWT
from app.core.database import get_database



router = APIRouter(tags=["Auth"], prefix="/auth")
session = Depends(get_database)


@router.post("/login")
def login(request: OAuth2PasswordRequestForm = Depends(), db = Depends(get_database)):
    user = db.users.find_one({"email": request.username})
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail=f"Account with this email does not exist"
        )

    # print(request.password, user['password'])
    if not Hash.verify(request.password, user['password']):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=f"Password does not match the email",
        )

    # access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = JWT.create_access_token(data={"sub": user['email']})
    return {"access_token": access_token, "token_type": "bearer"}

