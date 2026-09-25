import os

import psycopg
from dotenv import load_dotenv


# Load .env from the project root.
load_dotenv()


def get_connection() -> psycopg.Connection:
    """
    Create and return a connection to the Vestige PostgreSQL database.

    :return: A PostgreSQL connection
    """
    required_vars = (
        "AIVEN_PG_HOST",
        "AIVEN_PG_PORT",
        "AIVEN_PG_DATABASE",
        "AIVEN_PG_USER",
        "AIVEN_PG_PASSWORD",
    )

    missing_vars = [var for var in required_vars if not os.getenv(var)]

    if missing_vars:
        raise RuntimeError(
            f"Missing required environment variables: {', '.join(missing_vars)}"
        )

    return psycopg.connect(
        host=os.environ["AIVEN_PG_HOST"],
        port=int(os.environ["AIVEN_PG_PORT"]),
        dbname=os.environ["AIVEN_PG_DATABASE"],
        user=os.environ["AIVEN_PG_USER"],
        password=os.environ["AIVEN_PG_PASSWORD"],
        sslmode="require",
    )


if __name__ == "__main__":
    try:
        with get_connection() as connection:
            with connection.cursor() as cursor:
                cursor.execute("SELECT CURRENT_TIMESTAMP;")
                result = cursor.fetchone()

        print(f"Connection successful. Database time: {result[0]}")

    except Exception as exc:
        print(f"Database connection failed: {exc}")
        raise