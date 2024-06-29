from typing import Annotated

import jwt
from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials

from app.dto.auth import TokenData

__all__ = ["get_current_active_user_id"]

OAUTH2_SCHEME = HTTPBearer()
ALGORITHM = "HS256"


async def get_current_user(
    token: Annotated[HTTPAuthorizationCredentials, Depends(OAUTH2_SCHEME)]
) -> TokenData:
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(
            token.credentials,
            algorithms=[ALGORITHM],
            options={"verify_signature": False},
        )
        user_id: str = payload.get("sub")
        if user_id is None:
            raise credentials_exception
        return TokenData(sub=user_id)
    except jwt.InvalidTokenError:
        raise credentials_exception


async def get_current_active_user_id(
    current_user: Annotated[TokenData, Depends(get_current_user)]
) -> str:
    return current_user.sub
