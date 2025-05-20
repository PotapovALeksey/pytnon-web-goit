from pydantic import BaseModel
from typing import TypeVar, Generic

DataType = TypeVar("DataType")


class MetaSchema(BaseModel):
    total: int | None


class SingleResponseSchema(BaseModel, Generic[DataType]):
    data: DataType
    detail: str | None


class ListResponseSchema(BaseModel, Generic[DataType]):
    data: list[DataType]
    meta: MetaSchema
