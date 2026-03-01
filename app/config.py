from pydantic import BaseSettings

class Settings(BaseSettings):
    POSTGRES_DATABASE_PASSWORD: str
    POSTGRES_DATABASE_URL: str
    POSTGRES_PUBLISHABLE_KEY: str
    DATABASE_URL : str
    class Config:
        env_file = ".env"
settings = Settings()