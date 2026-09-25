from src.db.connection import get_connection
from src.db.schemas.dimensions import DIM_ASSET_SCHEMA, DIM_ASSET_CATEGORY_SCHEMA, DIM_TECHNICIAN_SCHEMA, \
    DIM_SITE_SCHEMA, DIM_FAILURE_MODE_SCHEMA, ASSET_CATEGORY_ASSIGNMENT_SCHEMA
from src.db.schemas.facts import FACT_MAINTENANCE_EVENT_SCHEMA, MAINTENANCE_EVENT_TECHNICIAN_SCHEMA, \
    MAINTENANCE_EVENT_FAILURE_MODE_SCHEMA


def create_schema() -> None:
    """
    Create the Vestige database schema.
    """
    with get_connection() as connection:
        with connection.cursor() as cursor:

            # Dimension schemas
            cursor.execute(DIM_ASSET_SCHEMA)
            cursor.execute(DIM_ASSET_CATEGORY_SCHEMA)
            cursor.execute(DIM_TECHNICIAN_SCHEMA)
            cursor.execute(DIM_SITE_SCHEMA)
            cursor.execute(DIM_FAILURE_MODE_SCHEMA)

            # Fact schemas
            cursor.execute(FACT_MAINTENANCE_EVENT_SCHEMA)

            # Link schemas
            cursor.execute(ASSET_CATEGORY_ASSIGNMENT_SCHEMA)
            cursor.execute(MAINTENANCE_EVENT_TECHNICIAN_SCHEMA)
            cursor.execute(MAINTENANCE_EVENT_FAILURE_MODE_SCHEMA)

        connection.commit()


if __name__ == "__main__":
    create_schema()
    print("Schema created successfully.")