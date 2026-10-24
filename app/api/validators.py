from fastapi import HTTPException
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.charity_project import CharityProject


async def check_project_exists(
    project_id: int,
    session: AsyncSession,
) -> CharityProject:
    project = await session.get(CharityProject, project_id)

    if project is None:
        raise HTTPException(
            status_code=404,
            detail='Проект не найден!',
        )

    return project


async def check_name_duplicate(
    name: str,
    session: AsyncSession,
    project_id: int | None = None,
) -> None:
    result = await session.execute(
        select(CharityProject).where(
            CharityProject.name == name
        )
    )

    project = result.scalars().first()

    if project is not None and project.id != project_id:
        raise HTTPException(
            status_code=400,
            detail='Проект с таким именем уже существует!',
        )


def check_project_not_closed(project: CharityProject) -> None:
    if project.fully_invested:
        raise HTTPException(
            status_code=400,
            detail='Закрытый проект нельзя редактировать!',
        )


def check_full_amount(
    new_amount: int,
    project: CharityProject,
) -> None:
    if new_amount < project.invested_amount:
        raise HTTPException(
            status_code=400,
            detail='Нелья установить значение full_amount меньше уже вложенной суммы.',
        )


def check_project_before_delete(project: CharityProject) -> None:
    if project.fully_invested or project.invested_amount > 0:
        raise HTTPException(
            status_code=400,
            detail='В проект были внесены средства, не подлежит удалению!',
        )
