from datetime import datetime

from sqlalchemy import Boolean, DateTime, Integer, String, Text
from sqlalchemy.orm import Mapped, mapped_column

from app.core.db import Base


class CharityProject(Base):
    __tablename__ = 'charityproject'

    id: Mapped[int] = mapped_column(
        Integer,
        primary_key=True
    )

    name: Mapped[str] = mapped_column(
        String(100),
        unique=True,
        nullable=False
    )

    description: Mapped[str] = mapped_column(Text, nullable=False)

    full_amount: Mapped[int] = mapped_column(Integer, nullable=False)

    invested_amount: Mapped[int] = mapped_column(Integer, nullable=False, default=0)

    fully_invested: Mapped[bool] = mapped_column(Boolean, default=False)

    create_date: Mapped[datetime] = mapped_column(DateTime, default=datetime.now)

    close_date: Mapped[datetime | None] = mapped_column(DateTime, nullable=True)