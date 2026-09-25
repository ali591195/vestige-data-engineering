def load_failure_mode(row: dict, connection) -> int:
    """
    Load one failure mode record into dim_failure_mode.

    :param row: One failure mode record containing only the name.
    :param connection: Active PostgreSQL connection.
    :return: The generated failure mode ID.
    """
    with connection.cursor() as cursor:
        cursor.execute(
            """
            INSERT INTO dim_failure_mode (name)
            VALUES (%s)
            RETURNING failure_mode_id;
            """,
            (row["name"],),
        )

        failure_mode_id = cursor.fetchone()[0]

    connection.commit()

    return failure_mode_id