from decouple import Csv, config
from dotenv import load_dotenv
from pydantic.main import BaseModel

load_dotenv()


class Settings(BaseModel):
    SECRET_KEY: str = config("SECRET_KEY")
    REST_APPLICATION_HOST: str = config("REST_APPLICATION_HOST")
    REST_APPLICATION_PORT: int = config("REST_APPLICATION_PORT")
    REST_APPLICATION_RELOAD: bool = config("REST_APPLICATION_RELOAD")
    REST_APPLICATION_WORKERS: int = config("REST_APPLICATION_WORKERS")
    REST_APPLICATION_NAME: str = config("REST_APPLICATION_NAME")
    REST_APPLICATION_DESCRIPTION: str = config("REST_APPLICATION_DESCRIPTION")
    APPLICATION_URL_CORS: str = config("APPLICATION_URL_CORS", cast=Csv())
    DATABASE_URI: str = config("DATABASE_URI")


settings = Settings()
