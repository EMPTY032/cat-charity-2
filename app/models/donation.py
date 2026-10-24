from datetime import datetime

from sqlalchemy import Boolean, DateTime, Integer, Text
from sqlalchemy.orm import Mapped, mapped_column

from app.core.db import Base


class Donation(Base):
    __tablename__ = 'donation'

    id: Mapped[int] = mapped_column(
        Integer,
        primary_key=True
    )

    comment: Mapped[str | None] = mapped_column(
        Text,
        nullable=True
    )

    full_amount: Mapped[int] = mapped_column(
        Integer,
        nullable=False
    )

    invested_amount: Mapped[int] = mapped_column(
        Integer,
        default=0
    )

    fully_invested: Mapped[bool] = mapped_column(
        Boolean,
        default=False
    )

    create_date: Mapped[datetime] = mapped_column(
        DateTime,
        default=datetime.now
    )

    close_date: Mapped[datetime | None] = mapped_column(
        DateTime,
        nullable=True
    )