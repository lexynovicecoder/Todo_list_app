from fastapi import  Response, Depends, HTTPException, status
from Models.models import *
from DTOs.dtos import CreateUserDTO, UserResponseDTO
from sqlmodel import Session,select
from database.database import *
from typing import List
from database.database import engine
from authorization_authentication.auth import bcrypt_context,JWT_SECRET_KEY,ALGORITHM
import jwt

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
    
    def login(self,username,password,db):
        user = db.query(User).filter(User.username == username).first()
        if not user and not bcrypt_context.verify(password, user.hashed_password) :
            return False
        return user
    
    def access_token(self,login_function):
        user = login_function
        if not user:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail='Could not validate user')
        token = self.create_access_token(user.username, user.id,timedelta(minutes=20))
        return {'access_token': token, 'token_type': 'bearer'}
    
    def create_access_token(self,username, user_id, expires_delta):
        encode = {'sub': username, 'id': user_id}
        expires = datetime.uctnow() + expires_delta
        return jwt.encode(encode, JWT_SECRET_KEY, algorithm=ALGORITHM)

            
