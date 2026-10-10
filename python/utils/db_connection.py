import os
from dotenv import load_dotenv
from sqlalchemy import create_engine

# Project root
PROJECT_ROOT = os.path.abspath(
    os.path.join(os.path.dirname(__file__), "..", "..")
)

# Load .env
load_dotenv(
    os.path.join(PROJECT_ROOT, ".env")
)


def get_engine():

    host = os.getenv("DB_HOST")
    port = os.getenv("DB_PORT")
    database = os.getenv("DB_NAME")
    username = os.getenv("DB_USER")
    password = os.getenv("DB_PASSWORD")

    if not all([host, port, database, username, password]):
        raise ValueError(
            "Database configuration is incomplete. "
            "Check your .env file."
        )

    connection_url = (
        f"mysql+pymysql://{username}:{password}"
        f"@{host}:{port}/{database}"
    )

    return create_engine(
        connection_url,
        pool_pre_ping=True
    )