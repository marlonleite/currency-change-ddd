from datetime import datetime

from pydantic.main import BaseModel, Field


class CurrencySchema(BaseModel):
    id: int
    code: str
    created_at: datetime
    updated_at: datetime

    class Config:
        orm_mode = True


class CreateCurrencySchema(BaseModel):
    code: str = Field(example="BRL")
