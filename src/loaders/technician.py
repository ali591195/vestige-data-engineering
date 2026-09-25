def load_technician(row: dict, connection) -> int:
    """
    Load one technician record into dim_technician.

    :param row: One technician record containing name, specialty, and hire date.
    :param connection: Active PostgreSQL connection.
    :return: The generated technician ID.
    """
    with connection.cursor() as cursor:
        cursor.execute(
            """
            INSERT INTO dim_technician (name, specialty, hire_date)
            VALUES (%s, %s, %s)
            RETURNING technician_id;
            """,
            (
                row["name"],
                row["specialty"],
                row["hire_date"],
            ),
        )

        technician_id = cursor.fetchone()[0]

    connection.commit()

    return technician_id