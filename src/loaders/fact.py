from datetime import date, timedelta
from random import randint


def load_fact(row: dict, connection) -> int:
    """
    Load one AI4I-style maintenance event and its relationships.

    :param row: One validated AI4I maintenance event.
    :param connection: Active PostgreSQL connection.
    :return: The generated event ID.
    """
    with connection.cursor() as cursor:
        cursor.execute(
            """
            SELECT
                (SELECT MIN(asset_id) FROM dim_asset),
                (SELECT MAX(asset_id) FROM dim_asset),
                (SELECT MIN(site_id) FROM dim_site),
                (SELECT MAX(site_id) FROM dim_site);
            """
        )

        asset_min, asset_max, site_min, site_max = cursor.fetchone()

        if asset_min is None or site_min is None:
            raise ValueError(
                "Cannot load maintenance event: "
                "asset or site dimension is empty."
            )

        asset_id = randint(asset_min, asset_max)
        site_id = randint(site_min, site_max)
        failure_date = date.today() - timedelta(days=randint(0, 5))

        cursor.execute(
            """
            WITH asset_categories AS (
                SELECT ac.category
                FROM asset_category_assignment aca
                JOIN dim_asset_category ac
                    ON ac.asset_category_id = aca.asset_category_id
                WHERE aca.asset_id = %s
            ),

            selected_technicians AS (
                SELECT DISTINCT ON (ac.category)
                    t.technician_id
                FROM asset_categories ac
                JOIN dim_technician t
                    ON t.specialty = ac.category
                ORDER BY
                    ac.category,
                    random()
            ),

            selected_failure_modes AS (
                SELECT failure_mode_id
                FROM dim_failure_mode
                WHERE name = ANY(%s::TEXT[])
            ),

            validation AS (
                SELECT
                    EXISTS (
                        SELECT 1
                        FROM dim_asset
                        WHERE asset_id = %s
                    ) AS asset_exists,

                    EXISTS (
                        SELECT 1
                        FROM dim_site
                        WHERE site_id = %s
                    ) AS site_exists,

                    (
                        SELECT COUNT(*)
                        FROM asset_categories
                    ) AS category_count,

                    (
                        SELECT COUNT(*)
                        FROM selected_technicians
                    ) AS technician_count,

                    (
                        SELECT COUNT(*)
                        FROM selected_failure_modes
                    ) AS failure_mode_count,

                    cardinality(%s::TEXT[]) AS failure_mode_input_count
            ),

            inserted_event AS (
                INSERT INTO fact_maintenance_event (
                    asset_id,
                    site_id,
                    failure_date,
                    air_temperature,
                    process_temperature,
                    rotational_speed,
                    torque,
                    tool_wear
                )
                SELECT
                    %s,
                    %s,
                    %s,
                    %s,
                    %s,
                    %s,
                    %s,
                    %s
                FROM validation
                WHERE asset_exists
                  AND site_exists
                  AND category_count > 0
                  AND category_count = technician_count
                  AND failure_mode_input_count > 0
                  AND failure_mode_count = failure_mode_input_count
                RETURNING event_id
            ),

            inserted_technicians AS (
                INSERT INTO maintenance_event_technician (
                    event_id,
                    technician_id
                )
                SELECT
                    ie.event_id,
                    st.technician_id
                FROM inserted_event ie
                CROSS JOIN selected_technicians st
                RETURNING event_id
            ),

            inserted_failure_modes AS (
                INSERT INTO maintenance_event_failure_mode (
                    event_id,
                    failure_mode_id
                )
                SELECT
                    ie.event_id,
                    sfm.failure_mode_id
                FROM inserted_event ie
                CROSS JOIN selected_failure_modes sfm
                RETURNING event_id
            )

            SELECT
                (SELECT event_id FROM inserted_event),
                asset_exists,
                site_exists,
                category_count,
                technician_count,
                failure_mode_count,
                failure_mode_input_count
            FROM validation;
            """,
            (
                asset_id,
                row["failure_modes"],
                asset_id,
                site_id,
                row["failure_modes"],
                asset_id,
                site_id,
                failure_date,
                row["air_temperature"],
                row["process_temperature"],
                row["rotational_speed"],
                row["torque"],
                row["tool_wear"],
            ),
        )

        (
            event_id,
            asset_exists,
            site_exists,
            category_count,
            technician_count,
            failure_mode_count,
            failure_mode_input_count,
        ) = cursor.fetchone()

        errors = []

        if not asset_exists:
            errors.append(f"Selected asset ID does not exist: {asset_id}")

        if not site_exists:
            errors.append(f"Selected site ID does not exist: {site_id}")

        if category_count != technician_count:
            errors.append(
                f"Not enough technicians for asset {asset_id}: "
                f"{category_count} categories, "
                f"{technician_count} matching technicians."
            )

        if failure_mode_count != failure_mode_input_count:
            errors.append(
                "One or more failure modes do not exist: "
                f"{row['failure_modes']}"
            )

        if event_id is None:
            errors.append(
                f"Maintenance event could not be inserted for asset {asset_id}."
            )

        if errors:
            raise ValueError("\n".join(errors))

    connection.commit()

    return event_id