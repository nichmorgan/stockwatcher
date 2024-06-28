from app.dto.base import BaseDto

__all__ = ["SimpleResponse"]


class SimpleResponse(BaseDto):
    message: str
