from Models.models import User
from authorization_authentication.auth import bcrypt_context,SECRET_KEY,ALGORITHM,oauth2_bearer
from typing import Annotated
from datetime import datetime, timedelta, timezone
from fastapi import status,Depends,HTTPException
from sqlmodel import select
from jose import jwt, JWTError



def user_post(dto, session):
    create_user_model = User(**dto.model_dump(), hashed_password=bcrypt_context.hash(dto.password))
    session.add(create_user_model)
    session.commit()

def authenticate_user(username:str, password:str, db):
    statement = select(User).where(User.username == username)
    user = db.exec(statement).first()
    if not user:
        return False
    if not bcrypt_context.verify(password, user.hashed_password):
        return False
    return user


def login_for_token(form,session):
    user = authenticate_user(form.username, form.password, session)
    if not user:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Could not validate user")
    token = create_access_token(user.username, user.id, timedelta(minutes=20))
    return {'access_token': token, 'token_type': 'bearer'}

def create_access_token(username:str, user_id:int, expires_delta: timedelta):
    encode = {'sub': username, 'id': user_id}
    expires = datetime.now(timezone.utc) + expires_delta
    encode.update({'exp': expires})
    return jwt.encode(encode, SECRET_KEY, algorithm=ALGORITHM)



def get_current_user(token: Annotated[str, Depends(oauth2_bearer)]):
    try:
        payload =jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get('sub')
        user_id: int =  payload.get('id')
        if username is None or user_id is None:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Could not validate credentials")
        return {'username': username, 'id': user_id}

    except JWTError:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Could not validate credentials")

