from typing import Annotated
from sqlmodel import Session
from database.database import engine
from fastapi import APIRouter,status,Depends,HTTPException
from fastapi.security import OAuth2PasswordRequestForm
from DTOs.dtos import CreateUserDTO
from services.user_service import *
from authorization_authentication.auth import Token,oauth2_bearer

router_user = APIRouter()

def get_session():
    with Session(engine) as session:
        yield session  # Yield the session for use in endpoints

@router_user.post("/", status_code=status.HTTP_201_CREATED)
def create_user(create_user_request: CreateUserDTO, session: Session = Depends(get_session)):
    user_post(create_user_request,session)

@router_user.post("/token", response_model=Token)
def login_for_access_token(form_data: Annotated[OAuth2PasswordRequestForm, Depends()],session: Session = Depends(get_session)):
    return login_for_token(form_data,session)

@router_user.get("/", status_code=status.HTTP_200_OK)
def user(user: dict = Depends(get_current_user), session: Session = Depends(get_session)):
    if user is None:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Authentication Failed")
    return {"User": user}  