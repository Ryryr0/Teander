import os

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file="C:/Users/artem/Desktop/traineeship/pet_project/Teander/api-gateway/.env"
    )  # not need in docker

    ALGORITHM: str

    # idk how to keep it correctly
    ORIGINS: list[str] = ["*"]

    PUBLIC_KEY: str = """
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

    AUTH_SERVICE: str


settings = Settings()


class URLS(str):
    auth_token_url = settings.AUTH_SERVICE + "users/token"
    auth_reg_url: str = settings.AUTH_SERVICE + "users/reg"
    auth_update_user_url = settings.AUTH_SERVICE + "users/update-user"
    auth_delete_user_url = settings.AUTH_SERVICE + "users/delete"
