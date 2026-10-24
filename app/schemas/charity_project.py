from datetime import datetime

from pydantic import BaseModel, ConfigDict, Field, model_validator


class CharityProjectBase(BaseModel):
    name: str = Field(min_length=5, max_length=100)
    description: str = Field(min_length=10)
    full_amount: int = Field(gt=0)

    model_config = ConfigDict(extra='forbid')


class CharityProjectCreate(CharityProjectBase):
    pass


class CharityProjectUpdate(BaseModel):
    name: str | None = Field(default=None, min_length=5, max_length=100)
    description: str | None = Field(default=None, min_length=10)
    full_amount: int | None = Field(default=None, gt=0)

    model_config = ConfigDict(extra='forbid')

    @model_validator(mode='after')
    def check_none_values(self):
        for field in self.model_fields_set:
            if getattr(self, field) is None:
                raise ValueError(
                    f'Поле {field} не может быть null'
                )
        return self


class CharityProjectDB(CharityProjectBase):
    id: int
    invested_amount: int
    fully_invested: bool
    create_date: datetime
    close_date: datetime | None = None

    model_config = ConfigDict(
        from_attributes=True,
        extra='forbid'
    )