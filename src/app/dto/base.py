import inflection
from sqlmodel import SQLModel
from pydantic import ConfigDict

__all__ = ["BaseDto"]


def alias_generator(value: str) -> str:
    return inflection.camelize(value, False)


class BaseDto(SQLModel, table=False):
    model_config = ConfigDict(
        populate_by_name=True,
        alias_generator=alias_generator,  # type: ignore
    )
