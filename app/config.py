import os
from dotenv import load_dotenv

load_dotenv()


class Config:
    BOT_TOKEN: str = os.getenv("BOT_TOKEN", "")

    DB_HOST: str = os.getenv("DB_HOST", "")
    DB_NAME: str = os.getenv("DB_NAME", "")
    DB_USER: str = os.getenv("DB_USER", "")
    DB_PORT: str = os.getenv("DB_PORT", "")
    DB_PASSWORD: str = os.getenv("DB_PASSWORD", "")
    DB_SSL: str = os.getenv("DB_SSL", "disable")

    @classmethod
    def validate(cls) -> bool:
        if not cls.BOT_TOKEN:
            return False
        if not all([cls.DB_HOST, cls.DB_NAME, cls.DB_USER, cls.DB_PASSWORD]):
            return False
        return True
