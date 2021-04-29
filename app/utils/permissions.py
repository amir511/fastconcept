from fastapi import Depends, HTTPException, status
from app.models.user import User
from app.utils.auth import authenticate_user


def is_admin(user: User = Depends(authenticate_user)):
    if not user or not user.is_admin:
        raise HTTPException(status.HTTP_401_UNAUTHORIZED,
                            detail='Only an admin can do such operation!.')
