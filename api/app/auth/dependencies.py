from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from jose import JWTError

from app.core.security import decode_jwt
from app.schemas.user import UserInDB
from app.services.exceptions import UserNotFoundError
from app.services.user_service import UserService
from app.api.v1.dependencies.user_deps import get_user_service


oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/router/login")

def get_current_user(
        token: str = Depends(oauth2_scheme),
        service: UserService = Depends(get_user_service)
) -> UserInDB:
    try:
        payload = decode_jwt(token=token)
    except JWTError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid token",
            headers={"WWW-Authenticate": "Bearer"}
        )

    username = payload.get("sub")
    if not username:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid token",
            headers={"WWW-Authenticate": "Bearer"}
        )

    try:
        user = service.get_user_by_username(username=username)
    except UserNotFoundError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="User not found",
            headers={"WWW-Authenticate": "Bearer"}
        )

    return user