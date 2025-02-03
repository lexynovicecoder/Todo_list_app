from pydantic import BaseModel
from fastapi.security import OAuth2PasswordBearer
import os
from dotenv import load_dotenv
from passlib.context import CryptContext
from sqlmodel import Session
from database.database import engine
from fastapi import APIRouter, Header
from typing import Annotated, Union



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



class Token(BaseModel):
    access_token: str
    token_type: str






