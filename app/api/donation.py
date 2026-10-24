from typing import Annotated

from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.db import get_async_session
from app.crud.donation import donation_crud
from app.schemas.donation import (
    DonationCreate,
    DonationDB,
    DonationFullInfoDB,
)
from app.services.investment import invest


router = APIRouter(
    prefix='/donation',
    tags=['donations'],
)

SessionDep = Annotated[AsyncSession, Depends(get_async_session)]


@router.get(
    '/',
    response_model=list[DonationFullInfoDB],
    summary='Получить список пожертвований',
)
async def get_all_donations(
    session: SessionDep,
):
    return await donation_crud.get_multi(session)


@router.post(
    '/',
    response_model=DonationDB,
    summary='Создать пожертвование',
)
async def create_donation(
    donation: DonationCreate,
    session: SessionDep,
):
    new_donation = await donation_crud.create(
        donation,
        session,
    )

    await invest(new_donation, session)

    await session.commit()
    await session.refresh(new_donation)

    return new_donation