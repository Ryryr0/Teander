from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file="C:/Users/artem/Desktop/traineeship/pet_project/Teander/profiles_service/.env"
    )  # not need in docker

    DB_HOST: str
    DB_PORT: int
    DB_USER: str
    DB_PASS: str
    DB_NAME: str

    REDIS_HOST: str
    REDIS_PORT: int
    REDIS_PASSWORD: str

    LOG_LVL: str

    @property
    def DATABASE_URL(self) -> str:
        # DSN
        return f"postgresql+asyncpg://{self.DB_USER}:{self.DB_PASS}@{self.DB_HOST}:{self.DB_PORT}/{self.DB_NAME}"


settings = Settings()
