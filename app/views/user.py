from fastapi import APIRouter, Depends, status, HTTPException, Response
from app.models.db_setup.session import get_db
from app.serializers.user import UserSerializerIn, UserSerializerOut
from app.models.user import User
from sqlalchemy.orm import Session
from app.utils.auth import authenticate_user

router = APIRouter(prefix='/user', tags=['Users'])

# CRUD
@router.post('/create/', response_model=UserSerializerOut, status_code=status.HTTP_201_CREATED)
def create_user(user: UserSerializerIn, db:Session=Depends(get_db)):
    user_obj = User(**user.dict())
    user_obj.set_password(user_obj.password)
    db.add(user_obj)
    db.commit()
    db.refresh(user_obj)
    return user_obj

@router.get('/get/{user_id}', response_model=UserSerializerOut)
def get_user(user_id:int, db:Session=Depends(get_db)):
    user_obj = db.query(User).get(user_id)
    if not user_obj:
        raise HTTPException(status.HTTP_404_NOT_FOUND, detail='User not found!')
    return user_obj

@router.get('/get/all/', response_model=list[UserSerializerOut])
def get_all_users(db:Session=Depends(get_db), user:User=Depends(authenticate_user)):
    return db.query(User).all()

@router.patch('/update/{user_id}', response_model=UserSerializerOut)
def update_user(user_id:int, user:UserSerializerIn, db:Session=Depends(get_db)):
    user_obj = db.query(User).get(user_id)
    if not user_obj:
        raise HTTPException(status.HTTP_404_NOT_FOUND, detail='User not found!')
    for k, v in user.dict(exclude_unset=True).items():
        if k == 'password':
            user_obj.set_password(v)
        else:
            setattr(user_obj, k, v)
    db.commit()
    db.refresh(user_obj)
    return user_obj

@router.delete('/delete/{user_id}', status_code=status.HTTP_204_NO_CONTENT, response_class=Response)
def delete_user(user_id:int, db:Session=Depends(get_db)):
    user_obj = db.query(User).get(user_id)
    if not user_obj:
        raise HTTPException(status.HTTP_404_NOT_FOUND, detail='User not found!')
    else:
        db.delete(user_obj)
        db.commit()