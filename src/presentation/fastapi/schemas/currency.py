from pydantic.main import BaseModel


class CurrencySchema(BaseModel):
    code: str
    name: str

    class Config:
        orm_mode = True
