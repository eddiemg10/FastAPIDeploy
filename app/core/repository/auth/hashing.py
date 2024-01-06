from passlib.context import CryptContext
from hashlib import sha256

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


class Hash:
    def encrypt(password: str):
        return pwd_context.hash(password)

    def verify(plain_password, hashed_password):
        return pwd_context.verify(plain_password, hashed_password)
    
    def sha256(key: str):
        # Generates a SHA256 hash
        return sha256(key.encode('utf-8')).hexdigest()