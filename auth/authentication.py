from fastapi import APIRouter,Depends,status,HTTPException
from fastapi.security import OAuth2PasswordRequestForm
from db.database import get_db
from sqlalchemy.orm.session import Session
from typing import Annotated
from db.models import DbUser
from db.hash import Hash
from auth import oauth2

db_dependancy = Annotated[Session,Depends(get_db)]

router = APIRouter(
    tags=['authentication']
)

@router.post('/token')
def get_token(db:db_dependancy,request: OAuth2PasswordRequestForm = Depends()):
    user = db.query(DbUser).filter(DbUser.username == request.username).first()
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail='Invide Cerdentials')
    if not Hash.verify_password(request.password,user.password):
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail='Incorrect password')
    access_token = oauth2.create_access_token(data={'sub':user.username})
    return {
        'access_token': access_token,
        'token_type': 'bearer',
        'username': user.username,
        'user_id': user.id
    }   