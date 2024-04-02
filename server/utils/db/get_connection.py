from utils.env_variable import env


def get_db_url_connection() -> str:
    connection_string = 'postgresql+psycopg2://{username}:{password}@{host}:{port}/{db_name}'

    return connection_string.format(
        username=env.DB_USERNAME,
        password=env.DB_PASSWORD,
        host=env.DB_HOST,
        port=env.DB_PORT,
        db_name=env.DB_NAME,
    )
