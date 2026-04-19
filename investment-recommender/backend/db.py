import psycopg2
from psycopg2.extensions import connection

import config


def get_db_connection() -> connection:
    return psycopg2.connect(
        host=config.DB_HOST,
        port=config.DB_PORT,
        dbname=config.DB_NAME,
        user=config.DB_USER,
        password=config.DB_PASS,
    )
