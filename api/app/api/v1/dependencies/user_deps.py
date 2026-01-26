from fastapi import Depends
from sqlalchemy.orm import Session

from app.core.db import get_db
from app.services.user_service import UserService


def get_user_service(db: Session = Depends(get_db)) -> UserService:
    return UserService(db=db)


