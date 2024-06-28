from sqlmodel import Field

from app.dto.base import BaseDto


class Token(BaseDto):
    access_token: str
    token_type: str


class TokenData(BaseDto):
    sub: str = Field(description="user id")
