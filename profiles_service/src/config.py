from functools import cached_property

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

    # For jwt token
    ALGORITHM: str

    @cached_property
    def DATABASE_URL(self) -> str:  # URl for sqlalchemy connection
        # DSN
        return f"postgresql+asyncpg://{self.DB_USER}:{self.DB_PASS}@{self.DB_HOST}:{self.DB_PORT}/{self.DB_NAME}"

    @cached_property
    async def PUBLIC_KEY(self) -> str:
        """Receive public key from kafka"""
        return """
        -----BEGIN PUBLIC KEY-----
        MIIBIjANBgkqhkiG9w0BAQEFAAOCAQ8AMIIBCgKCAQEAyrt9oclp166oK5lB0jmy
        N1FwiO1vgO9HGJgLD59UXRjJgEuoP0HYBNgmoOAFNMRp8C5Tgog+NCGEn8+CoGSD
        WJU6Mb/HHnK+p8Q/SflbRkLPobJcW7k17+InpNiJzDsOpS6GT845+1Z2k03nacLl
        Ni2jLfD0pv3TdZWEH7IK1OeX5koEqIPwRtAPSbc6zSzE1GfxPm9+g6md633rwGpz
        dvG9djm1m+6yVirKE9iTr2Zy5G5unIHLKxmQ0q8Pp0PIiUjK2iw5F9lMaIICIOp0
        HYgdoaq9Rmy3KAVUHebuQosAONdXFFx/4LXarSqmoeS/z1M4mJijIHdKofmQGVBs
        SQIDAQAB
        -----END PUBLIC KEY-----
        """


settings = Settings()
