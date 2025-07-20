import os

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    # model_config = SettingsConfigDict(
    #     env_file="C:/Users/artem/Desktop/traineeship/pet_project/Teander/auth_service/.env"
    # )  # not need in docker

    DB_HOST: str
    DB_PORT: int
    DB_USER: str
    DB_PASS: str
    DB_NAME: str

    PRIVATE_KEY_PATH: str
    PUBLIC_KEY_PATH: str
    ALGORITHM: str
    ACCESS_TOKEN_EXPIRE_MINUTES: int

    # idk how to keep it correctly
    ORIGINS: list[str] = ["*"]

    @property
    def DATABASE_URL(self) -> str:
        # DSN
        return f"postgresql+asyncpg://{self.DB_USER}:{self.DB_PASS}@{self.DB_HOST}:{self.DB_PORT}/{self.DB_NAME}"

    @property
    def PRIVATE_KEY(self) -> bytes:
        with open(os.path.join(os.path.dirname(os.path.abspath(__file__)), "../keys/private.pem"), "rb") as f:
            return f.read()

    @property
    def PUBLIC_KEY(self) -> bytes:
        with open(os.path.join(os.path.dirname(os.path.abspath(__file__)), "../keys/public.pem"), "rb") as f:
            return f.read()


settings = Settings()
