from pydantic import BaseModel, EmailStr, Field
from typing import Optional
from datetime import datetime


class UserBase(BaseModel):
    id: int
    username: str
    email: Optional[EmailStr] = None


class UserCreate(UserBase):
    password: str = Field(min_length=5, max_length=64)


class UserRead(UserBase):
    pass
    # model_config = {"from_attributes": True}


class UserInDB(UserBase):
    hashed_password: str
    created_at: datetime




