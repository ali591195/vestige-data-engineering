def load_asset(row: dict, connection) -> int:
    """
    Load one synthetic asset and its category relationships.

    :param row: One validated asset record containing asset categories and
                install date.
    :param connection: Active PostgreSQL connection.
    :return: The generated asset ID.
    """
    with connection.cursor() as cursor:
        cursor.execute(
            """
            SELECT asset_category_id
            FROM dim_asset_category
            WHERE category = ANY(%s);
            """,
            (row["asset_category"],),
        )

        category_ids = [result[0] for result in cursor.fetchall()]

        if len(category_ids) != len(row["asset_category"]):
            raise ValueError(
                f"One or more asset categories do not exist: "
                f"{row['asset_category']}"
            )

        cursor.execute(
            """
            WITH inserted_asset AS (
                INSERT INTO dim_asset (install_date)
                VALUES (%s)
                RETURNING asset_id
            )
            INSERT INTO asset_category_assignment (
                asset_id,
                asset_category_id
            )
            SELECT
                inserted_asset.asset_id,
                category_id
            FROM inserted_asset
            CROSS JOIN UNNEST(%s::INTEGER[]) AS categories(category_id)
            RETURNING asset_id;
            """,
            (
                row["install_date"],
                category_ids,
            ),
        )

        asset_id = cursor.fetchone()[0]

    connection.commit()

    return asset_id