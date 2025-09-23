from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from ..database import get_database
from ..models.user import User
from .auth import verify_token

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="api/auth/login")

async def get_current_user(token: str = Depends(oauth2_scheme)):
    db = get_database()
    if db is None:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Database connection failed"
        )
    
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    
    username = verify_token(token, credentials_exception)
    user = await db.users.find_one({"username": username})
    if user is None:
        raise credentials_exception
    
    # Convert to User model-like object for compatibility
    class UserObj:
        def __init__(self, user_doc):
            self.id = str(user_doc["_id"])
            self.username = user_doc["username"]
            self.email = user_doc["email"]
            self.is_active = user_doc["is_active"]
            self.created_at = user_doc["created_at"]
    
    return UserObj(user)