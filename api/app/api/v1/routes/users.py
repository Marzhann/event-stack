from fastapi import APIRouter, status, Depends, HTTPException
from typing import List

from api.app.api.v1.dependencies.user_deps import get_user_service
from api.app.schemas.user import UserRead, UserCreate
from api.app.services.exceptions import UserAlreadyExistError
from api.app.services.user_service import UserService


router = APIRouter()


@router.post("", response_model=UserRead, status_code=status.HTTP_201_CREATED)
def create_user(
        user_in: UserCreate,
        service: UserService = Depends(get_user_service)
) -> UserRead:
    try:
        return service.create(user=user_in)
    except UserAlreadyExistError:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="User with the same name already exists"
        )


@router.get("", response_model=List[UserRead])
def list_users(service: UserService = Depends(get_user_service)) -> List[UserRead]:
    return service.list()


# @router.get("/{user_id}")
# def get_user(user_id:int):
#     pass
