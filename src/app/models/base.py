from app.dto.base import BaseDto

__all__ = ["BaseModel"]


class BaseModel(BaseDto, table=True): ...
