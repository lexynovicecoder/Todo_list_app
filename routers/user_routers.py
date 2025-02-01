from fastapi import APIRouter, Depends
from DTOs.dtos import CreateUserDTO, UserResponseDTO
from services.user_service import user_service, UserServices
from authorization_authentication.auth import Token
from fastapi.security import OAuth2PasswordRequestForm
from typing import Annotated
from Models.models import User

router_user = APIRouter(tags=["Auth"])

@router_user.post("/create_user", response_model=UserResponseDTO)
def user_create(user_DTO: CreateUserDTO,user_service: UserServices = Depends(user_service)):
    user = user_service.create_user(user_DTO)
    return user

@router_user.post("/login", response_model=Token)
def login(form_data: Annotated[OAuth2PasswordRequestForm, Depends()],user_service: UserServices = Depends(user_service)):
    authentication = user_service.login(form_data.username, form_data.password,User)
    token = user_service.access_token(authentication)
    return token
    
