
from fastapi import HTTPException, status, Security, FastAPI, Depends   
from fastapi.security import APIKeyHeader, APIKeyQuery
from app.core.database import get_database

from app.core.repository.auth.hashing import Hash
from app.core.repository.serialize import serializeDict

api_key_header = APIKeyHeader(name="x-api-key", auto_error=False)
db = get_database()

def get_api_key(
        api_key_header: str = Security(api_key_header),
) -> str:
    if api_key_header:
        hashed_key = Hash.sha256(api_key_header)
        # Check if hashed key exists in DB
        api_key = db.apikeys.find_one({"value": hashed_key})
        if api_key and api_key['active']:
            return serializeDict(api_key)
    raise HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Invalid or missing API Key",
    )