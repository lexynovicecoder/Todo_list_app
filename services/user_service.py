from fastapi import  Response, Depends, HTTPException, status
from Models.models import *
from DTOs.dtos import CreateUserDTO, UserResponseDTO
from sqlmodel import Session,select
from database.database import *
from typing import List
from database.database import engine
from authorization_authentication.auth import bcrypt_context

def get_session():
    with Session(engine) as session:
        yield session  # Yield the session for use in endpoints

def user_service(response: Response, session: Session = Depends(get_session)):
    return UserServices(session=session, response=response)
    
class UserServices:
    def __init__(self,session,response):
        self.session = session  # Database session
        self.response = response
    
    def create_user(self,create_dto):
        user = User(username=create_dto.username, hashed_password=bcrypt_context.hash(create_dto.password), 
                           first_name=create_dto.first_name, last_name=create_dto.last_name, email=create_dto.email)
       
        self.session.add(user)
        self.session.commit()
        self.session.refresh(user)
        self.response.status_code = status.HTTP_201_CREATED
        return user
