from contextlib import asynccontextmanager

from fastapi import FastAPI

from app.api import main_router
from app.core.config import settings
from app.core.db import Base, engine
from app.models.charity_project import CharityProject
from app.models.donation import Donation


@asynccontextmanager
async def lifespan(app: FastAPI):
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    yield


app = FastAPI(
    title=settings.app_title,
    description='API благотворительного фонда поддержки котиков',
    version='0.1.0',
    lifespan=lifespan,
)

app.include_router(main_router)