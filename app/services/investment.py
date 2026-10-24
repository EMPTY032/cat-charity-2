from datetime import datetime

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.charity_project import CharityProject
from app.models.donation import Donation


async def invest(
    new_obj: CharityProject | Donation,
    session: AsyncSession
):
    if isinstance(new_obj, CharityProject):
        model = Donation
    else:
        model = CharityProject

    objects = await session.execute(
        select(model)
        .where(model.fully_invested.is_(False))
        .order_by(model.create_date, model.id)
    )

    open_objects = objects.scalars().all()

    for obj in open_objects:
        new_remaining = new_obj.full_amount - new_obj.invested_amount
        obj_remaining = obj.full_amount - obj.invested_amount

        amount = min(new_remaining, obj_remaining)

        new_obj.invested_amount += amount
        obj.invested_amount += amount

        if obj.invested_amount == obj.full_amount:
            obj.fully_invested = True
            obj.close_date = datetime.now()

        if new_obj.invested_amount == new_obj.full_amount:
            new_obj.fully_invested = True
            new_obj.close_date = datetime.now()
            break

    return new_obj