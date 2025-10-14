from fastapi import APIRouter,Depends
from schemas import UserBase,UserDisplay
from sqlalchemy.orm.session import Session
from db.database import get_db
from db import db_user
from typing import List
from auth.oauth2 import get_current_user

router=APIRouter(
    prefix='/user',
    tags=['user']
)
# create user
@router.post('/',response_model=UserDisplay)
def create_user(request: UserBase,db: Session=Depends(get_db)):
    return db_user.create_user(db,request)

#Read all user
@router.get('/',response_model=List[UserDisplay])
def get_all_user(db:Session=Depends(get_db)):
    return db_user.get_all_user(db)

#Read by ID
@router.get('/{id}',response_model=UserDisplay)
def get_user(id: int,db:Session=Depends(get_db),current_user:UserBase=Depends(get_current_user)):
    return db_user.get_user(db,id)

@router.post('/{id}/Update')
def update_user(id: int,request: UserBase,db:Session=Depends(get_db),current_user:UserBase=Depends(get_current_user)):
    return db_user.update_user(db,id,request)

@router.get('/{id}/Deleted')
def delete_user(id: int,db:Session=Depends(get_db),current_user:UserBase=Depends(get_current_user)):
    return db_user.delete_user(db,id)