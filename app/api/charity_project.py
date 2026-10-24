from typing import Annotated

from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.db import get_async_session
from app.crud.charity_project import charity_project_crud
from app.schemas.charity_project import (
    CharityProjectCreate,
    CharityProjectDB,
)
from app.services.investment import invest

from app.api.validators import (
    check_full_amount,
    check_name_duplicate,
    check_project_before_delete,
    check_project_exists,
    check_project_not_closed,
)
from app.schemas.charity_project import CharityProjectUpdate
from datetime import datetime


router = APIRouter(
    prefix='/charity_project',
    tags=['charity_projects'],
)

SessionDep = Annotated[AsyncSession, Depends(get_async_session)]


@router.get(
    '/',
    response_model=list[CharityProjectDB],
    summary='Получить список проектов',
)
async def get_all_charity_projects(
    session: SessionDep,
):
    return await charity_project_crud.get_multi(session)


@router.post(
    '/',
    response_model=CharityProjectDB,
    summary='Создать благотворительный проект',
)
async def create_charity_project(
    project: CharityProjectCreate,
    session: SessionDep,
):
    await check_name_duplicate(project.name, session)

    new_project = await charity_project_crud.create(
        project,
        session,
    )

    await invest(new_project, session)

    await session.commit()
    await session.refresh(new_project)

    return new_project


@router.patch(
    '/{project_id}',
    response_model=CharityProjectDB,
    summary='Редактировать проект',
)
async def update_charity_project(
    project_id: int,
    project_in: CharityProjectUpdate,
    session: SessionDep,
):
    project = await check_project_exists(project_id, session)

    check_project_not_closed(project)

    if project_in.name is not None:
        await check_name_duplicate(
            project_in.name,
            session,
            project_id,
        )

    if project_in.full_amount is not None:
        check_full_amount(
            project_in.full_amount,
            project,
        )

    project = await charity_project_crud.update(
        project,
        project_in,
        session,
    )

    if project.invested_amount == project.full_amount:
        project.fully_invested = True
        project.close_date = datetime.now()

    await session.commit()
    await session.refresh(project)

    return project


@router.delete(
    '/{project_id}',
    response_model=CharityProjectDB,
    summary='Удалить проект',
)
async def delete_charity_project(
    project_id: int,
    session: SessionDep,
):
    project = await check_project_exists(project_id, session)

    check_project_before_delete(project)

    deleted_project = await charity_project_crud.remove(
        project,
        session,
    )

    await session.commit()

    return deleted_project