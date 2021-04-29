from fastapi.security import OAuth2PasswordRequestForm
from fastapi import APIRouter, status, Depends, HTTPException
from app.models.user import User
from app.models.db_setup.session import get_db
from sqlalchemy.orm import Session
from app.utils.auth import JWTHelper, authenticate_user

router = APIRouter(prefix='/auth', tags=['Auth'])

@router.post('/login/', status_code=status.HTTP_200_OK)
def login(form_data:OAuth2PasswordRequestForm=Depends(), db:Session=Depends(get_db)):
    user_obj = db.query(User).filter(User.username==form_data.username).first()
    if not user_obj:
        raise HTTPException(status.HTTP_404_NOT_FOUND, detail='User not found!')
    is_valid = user_obj.verify_password(form_data.password)
    if not is_valid:
        raise HTTPException(status.HTTP_401_UNAUTHORIZED, detail='Incorrect password!')
    access, refresh = JWTHelper.generate_access_and_refresh_tokens(form_data.username)
    return {
        'access_token':access,
        'refresh_token':refresh
    }

        

@router.post('/refresh/', status_code=status.HTTP_200_OK)
def refresh_token(refresh_token: str):
    jwt_helper = JWTHelper(refresh_token=refresh_token)
    access_token = jwt_helper.refresh_access_token()
    return {'access_token': access_token}