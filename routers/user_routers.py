from fastapi import APIRouter, Depends
from DTOs.dtos import CreateUserDTO, UserResponseDTO
from services.user_service import user_service, UserServices

router_user = APIRouter(tags=["Auth"])

@router_user.post("/create_user", response_model=UserResponseDTO)
def user_create(user_DTO: CreateUserDTO,user_service: UserServices = Depends(user_service)):
    user = user_service.create_user(user_DTO)
    return user