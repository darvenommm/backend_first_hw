"""Module for working with env variables."""
from os import environ

from dotenv import load_dotenv

load_dotenv()


class NotFoundEnvVariableError(Exception):
    """Error for not founding env variable."""

    def __init__(self, variable_name: str, *args: object) -> None:
        super().__init__(f'Not found {variable_name} environment variable!', *args)


SERVER_HOST = environ.get('SERVER_HOST', '127.0.0.1')
SERVER_PORT = int(environ.get('SERVER_PORT', '8000'))
SERVER_PROTOCOL = environ.get('SERVER_PROTOCOL', 'http')
SERVER_DOMAIN = f'{SERVER_PROTOCOL}://{SERVER_HOST}:{SERVER_PORT}'
DB_NAME = environ.get('DB_NAME', 'postgres')
DB_HOST = environ.get('DB_HOST', '127.0.0.1')
DB_PORT = int(environ.get('DB_PORT', '5432'))
DB_USERNAME = environ.get('DB_USERNAME', 'postgres')
DB_PASSWORD = environ.get('DB_PASSWORD', '')
MOVIES_API_KEY = environ.get('MOVIES_API_KEY', '')


if not DB_PASSWORD:
    raise NotFoundEnvVariableError('DB_PASSWORD')

if not MOVIES_API_KEY:
    raise NotFoundEnvVariableError('MOVIES_API_KEY')
