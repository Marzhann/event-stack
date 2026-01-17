from pydantic.v1 import EmailStr
from typing import List
from sqlalchemy.orm import Session

from api.app.core.security import verify_password, get_password_hash
from api.app.schemas.user import UserInDB, UserCreate, UserRead
from api.app.services.exceptions import UserNotFoundError, WrongUserPassword, UserAlreadyExistError
from api.app.models.user import User


class UserService:
    def __init__(self, db: Session):
        self.db = db


    def get_user_by_username(self, username: str) -> UserInDB:
        user = (
            self.db.query(User)
            .filter(User.username == username)
            .first()
        )
        if not user:
            raise UserNotFoundError(f"User {username} not found")
        return UserInDB.model_validate(user, from_attributes=True)


    def authenticate_user(self, username: str, password: str) -> UserInDB:
        user = self.get_user_by_username(username=username)
        if not verify_password(plain_password=password, hashed_password=user.hashed_password):
            raise WrongUserPassword(f"Wrong password for user {username}")
        return user


    def create(self, user: UserCreate) -> UserRead:
        # check if user is already created
        try:
            if self.get_user_by_username(username=user.username):
                raise UserAlreadyExistError(f"User {user.username} already exist")
        except UserNotFoundError:
            pass

        user = User(
            username=user.username,
            email=EmailStr(user.email),
            hashed_password=get_password_hash(user.password)
        )

        self.db.add(user)
        self.db.commit()
        self.db.refresh(user)

        # return clean version without hashed password and metadata
        return UserRead.model_validate(user, from_attributes=True)


    def list(self) -> List[UserRead]:
        users = self.db.query(User).all()
        return [
            UserRead.model_validate(user, from_attributes=True)
            for user in users
        ]

