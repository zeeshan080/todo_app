from starlette.config import Config
from starlette.datastructures import Secret
try:
   config = Config(".env")
except FileNotFoundError:
   config = Config()
DATABASE_URL = config("DATABASE_URL", cast=Secret)
DATABASE_URL_TEST = config("DATABASE_URL_TEST", cast=Secret)

SECRET_KEY = config("SECRET_KEY", cast=Secret)
API_V1_STR = "/api/v1"
ACCESS_TOKEN_EXPIRE_MINUTES=30   