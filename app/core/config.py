from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    app_title: str = 'Благотворительный фонд QRKot'
    database_url: str = 'sqlite+aiosqlite:///./fastapi.db'


settings = Settings()