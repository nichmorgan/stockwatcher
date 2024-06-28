import inflection
from sqlmodel import SQLModel

__all__ = ["BaseDto"]


def alias_generator(value: str) -> str:
    return inflection.camelize(value, False)


class BaseDto(SQLModel, table=False, alias_generator=alias_generator): ...
