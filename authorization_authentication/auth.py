from jose import jwt, JWTError
from pydantic import BaseModel
from fastapi.security import OAuth2PasswordBearer,OAuth2PasswordRequestForm
import os
from datetime import datetime, timedelta, timezone
from dotenv import load_dotenv
from passlib.context import CryptContext
from typing import Annotated
from sqlmodel import Session,select
from database.database import engine
from fastapi import APIRouter,status,Depends,HTTPException
from Models.models import User


router_user = APIRouter()

load_dotenv()

SECRET_KEY = os.getenv("SECRET_KEY")
ALGORITHM = os.getenv("ALGORITHM")
ACCESS_TOKEN_EXPIRE_MINUTES = 60

bcrypt_context = CryptContext(schemes=["bcrypt"], deprecated="auto") # helps hash passwords
oauth2_bearer = OAuth2PasswordBearer(tokenUrl="auth/token")

def get_session():
    with Session(engine) as session:
        yield session  # Yield the session for use in endpoints


class CreateUserDTO(BaseModel):
    username: str
    password: str
class Token(BaseModel):
    access_token: str
    token_type: str


@router_user.post("/", status_code=status.HTTP_201_CREATED)
def create_user(create_user_request: CreateUserDTO, session: Session = Depends(get_session)):
    create_user_model = User(username=create_user_request.username, hashed_password=bcrypt_context.hash(create_user_request.password))
    session.add(create_user_model)
    session.commit()

@router_user.post("/token", response_model=Token)
def login_for_access_token(form_data: Annotated[OAuth2PasswordRequestForm, Depends()],session: Session = Depends(get_session)):
    user = authenticate_user(form_data.username, form_data.password, session)
    if not user:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Could not validate user")
    token = create_access_token(user.username, user.id, timedelta(minutes=20))
    return {'access_token': token, 'token_type': 'bearer'}

def create_access_token(username:str, user_id:int, expires_delta: timedelta):
    encode = {'sub': username, 'id': user_id}
    expires = datetime.now(timezone.utc) + expires_delta
    encode.update({'exp': expires})
    return jwt.encode(encode, SECRET_KEY, algorithm=ALGORITHM)

def authenticate_user(username:str, password:str, db):
    statement = select(User).where(User.username == username)
    user = db.exec(statement).first()
    if not user:
        return False
    if not bcrypt_context.verify(password, user.hashed_password):
        return False
    return user

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


@router_user.get("/", status_code=status.HTTP_200_OK)
def user(user: dict = Depends(get_current_user), session: Session = Depends(get_session)):
    if user is None:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Authentication Failed")
    return {"User": user}  