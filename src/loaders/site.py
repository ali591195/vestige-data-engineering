def load_site(row: dict, connection) -> int:
    """
    Load one site record into dim_site.

    :param row: One site record containing site name, address, and city.
    :param connection: Active PostgreSQL connection.
    :return: The generated site ID.
    """
    with connection.cursor() as cursor:
        cursor.execute(
            """
            INSERT INTO dim_site (site_name, address, city)
            VALUES (%s, %s, %s)
            RETURNING site_id;
            """,
            (
                row["site_name"],
                row["address"],
                row["city"],
            ),
        )

        site_id = cursor.fetchone()[0]

    connection.commit()

    return site_id