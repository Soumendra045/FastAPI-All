from fastapi.security import OAuth2PasswordBearer
from jose import jwt,JWTError
from typing import Optional
from datetime import datetime,timedelta
from fastapi import Depends,status,HTTPException
from db.database import get_db
from sqlalchemy.orm.session import Session
from db import db_user


oauth2_scheme = OAuth2PasswordBearer(tokenUrl='token')

SECRET_KEY = '77407c7339a6c00544e51af1101c4abb4aea2a31157ca5f7dfd87da02a628107'
ALGORITHM = 'HS256'
ACCESS_TOKEN_EXPIRE_MINUTES = 30

def create_access_token(data: dict,expire_delta: Optional[timedelta] = None):
    to_encode = data.copy()
    if expire_delta:
        expire = datetime.utcnow()+expire_delta
    else:
        expire = datetime.utcnow()+timedelta(minutes=15)
    
    to_encode.update({"exp":expire})
    encode_jwt = jwt.encode(to_encode,SECRET_KEY,algorithm=ALGORITHM)
    return encode_jwt


def get_current_user(token: str = Depends(oauth2_scheme),db: Session=Depends(get_db)):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail='Could not validate User',
        headers={'WWW-authenticated':'Bearer'}
    )
    try:
        payload = jwt.decode(token,SECRET_KEY,algorithms=[ALGORITHM])
        username: str = payload.get('sub')
        if username is None:
            raise credentials_exception
    except JWTError:
        raise credentials_exception
    user = db_user.get_user_by_username(db,username=username)

    if user is None:
        raise credentials_exception
    
    return user 