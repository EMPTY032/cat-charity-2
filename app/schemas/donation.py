from datetime import datetime

from pydantic import BaseModel, ConfigDict, Field


class DonationCreate(BaseModel):
    full_amount: int = Field(gt=0)
    comment: str | None = None

    model_config = ConfigDict(extra='forbid')


class DonationDB(DonationCreate):
    id: int
    create_date: datetime

    model_config = ConfigDict(
        from_attributes=True,
        extra='forbid'
    )


class DonationFullInfoDB(DonationDB):
    invested_amount: int
    fully_invested: bool
    close_date: datetime | None = None