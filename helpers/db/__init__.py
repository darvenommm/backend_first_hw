from os import environ


def get_db_url_connection() -> str:
    db_name = environ.get('DB_NAME', 'postgres')
    host = environ.get('DB_HOST', '127.0.0.1')
    port = int(environ.get('DB_PORT', '5432'))
    username = environ.get('DB_USERNAME', 'postgres')
    password = environ.get('DB_PASSWORD')

    if password is None:
        raise ValueError('Not found password in .env file')

    return f'postgresql+psycopg2://{username}:{password}@{host}:{port}/{db_name}'


__all__ = ('get_db_url_connection',)
