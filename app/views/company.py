from fastapi import APIRouter, Depends
from app.models.db_setup.session import get_db
from app.serializers.company import CompanySerializerIn, CompanySerializerOut
from app.models.company import Company
from sqlalchemy.orm import Session
from fastapi import status, HTTPException, Response
from typing import List
from app.utils.auth import authenticate_user
from app.utils.permissions import is_admin

router = APIRouter(prefix='/company', tags=['Companies'], dependencies=[Depends(authenticate_user)])

@router.post('/create/', response_model=CompanySerializerOut, status_code=status.HTTP_201_CREATED, dependencies=[Depends(is_admin)])
def create_company(company:CompanySerializerIn, db:Session=Depends(get_db)):
    company_obj = Company(**company.dict())
    db.add(company_obj)
    db.commit()
    db.refresh(company_obj)
    return company_obj

@router.get('/get/{company_id}', response_model=CompanySerializerOut)
def get_company(company_id:int, db:Session=Depends(get_db)):
    company_obj = db.query(Company).get(company_id)
    if not company_obj:
        raise HTTPException(status.HTTP_404_NOT_FOUND, detail='Company not found')
    return company_obj


@router.get('/get/all/', response_model=List[CompanySerializerOut])
def get_all_companies(db:Session=Depends(get_db)):
    return db.query(Company).all()

@router.patch('/update/{company_id}', response_model=CompanySerializerOut)
def update_company(company_id:int, company:CompanySerializerIn, db:Session=Depends(get_db)):
    company_obj = db.query(Company).get(company_id)
    if not company_obj:
        raise HTTPException(status.HTTP_404_NOT_FOUND, detail='Company not found')
    for k, v in company.dict(exclude_unset=True).items():
        setattr(company_obj, k, v)

    db.commit()
    db.refresh(company_obj)
    return company_obj

@router.delete('/delete/{company_id}', status_code=status.HTTP_204_NO_CONTENT, response_class=Response, dependencies=[Depends(is_admin)])
def delete_company(company_id:int, db:Session=Depends(get_db)):
    company_obj = db.query(Company).get(company_id)
    if not company_obj:
        raise HTTPException(status.HTTP_404_NOT_FOUND, detail='Company not found!')
    else:
        db.delete(company_obj)
        db.commit()