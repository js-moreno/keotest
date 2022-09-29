
from pydantic import BaseModel


class RecordBase(BaseModel):
    array: str
    result: int


class RecordCreate(RecordBase):
    pass


class Record(RecordBase):
    id: int

    class Config:
        orm_mode = True