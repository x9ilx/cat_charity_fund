from typing import Optional

from pydantic import BaseModel, Extra, Field, PositiveInt, validator

from app.schemas.mixins import DonationMixinSchema


class CharityProjectBase(BaseModel):
    name: str = Field(..., min_length=1, max_length=100)
    description: str
    full_amount: PositiveInt

    @validator('description')
    def not_empty_description(cls, value):
        if not value:
            raise ValueError('Описание не может быть пустым')
        return value


class CharityProjectCreate(CharityProjectBase):
    ...


class CharityProjectUpdate(CharityProjectBase):
    name: Optional[str] = Field(None, min_length=1, max_length=100)
    description: Optional[str]
    full_amount: Optional[PositiveInt]

    class Config:
        extra = Extra.forbid


class CharityProjectDB(DonationMixinSchema, CharityProjectBase):
    id: int

    class Config:
        orm_mode = True
