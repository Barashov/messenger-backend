from pydantic import BaseSettings
import os
from dotenv import load_dotenv

load_dotenv()


class Settings(BaseSettings):
    salt: str = 'secret_salt'
    key: str = 'secret_key'

    class Config:
        env_file = os.path.expanduser('~/.env')


settings = Settings()
