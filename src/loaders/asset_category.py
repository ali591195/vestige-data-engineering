def load_asset_category(row: dict, connection) -> int:
    """
    Load one asset category record into dim_asset_category.

    :param row: One asset category record containing only the category.
    :param connection: Active PostgreSQL connection.
    :return: The generated asset category ID.
    """
    with connection.cursor() as cursor:
        cursor.execute(
            """
            INSERT INTO dim_asset_category (category)
            VALUES (%s)
            RETURNING asset_category_id;
            """,
            (row["category"],),
        )

        asset_category_id = cursor.fetchone()[0]

    connection.commit()

    return asset_category_id