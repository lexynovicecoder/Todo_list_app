from pydantic import BaseModel
from fastapi.security import OAuth2PasswordBearer, HTTPAuthorizationCredentials, HTTPBearer
import os
from dotenv import load_dotenv
from passlib.context import CryptContext
from sqlmodel import Session
from database.database import engine
from fastapi import APIRouter, Header, HTTPException, Depends,status
from typing import Annotated, Union
import jwt


router_user = APIRouter()

load_dotenv()

SECRET_KEY = os.getenv("SECRET_KEY")
ALGORITHM = os.getenv("ALGORITHM")
ACCESS_TOKEN_EXPIRE_MINUTES = 60



bcrypt_context = CryptContext(schemes=["bcrypt"], deprecated="auto") # helps hash passwords

def get_session():
    with Session(engine) as session:
        yield session  # Yield the session for use in endpoints


security_scheme = HTTPBearer()

class Token(BaseModel):
    access_token: str
    token_type: str



async def jwt_decode_token(credentials: HTTPAuthorizationCredentials = Depends(security_scheme)):
    if credentials.scheme != "Bearer":
        raise HTTPException(status_code=401, detail="Invalid authentication scheme")
    try:
        payload = jwt.decode(credentials.credentials, SECRET_KEY, algorithms=[ALGORITHM], issuer=None,
                             leeway=0, options={"verify_aud": False, "verify_signature": True})
        print(payload)
        return payload
    except jwt.exceptions.DecodeError as error:
        raise HTTPException(status_code=401, detail=error.__str__())
    except jwt.exceptions.ExpiredSignatureError:
        raise HTTPException(status_code=401, detail="Token has expired")
    