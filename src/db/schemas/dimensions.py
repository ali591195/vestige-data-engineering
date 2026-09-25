from psycopg import sql

from src.constants import ASSET_CATEGORIES, FAILURE_MODES

ASSET_CATEGORY_VALUES = sql.SQL(", ").join(
    sql.Literal(category) for category in ASSET_CATEGORIES
)

FAILURE_MODE_VALUES = sql.SQL(", ").join(
    sql.Literal(failure) for failure in FAILURE_MODES
)

# Dimension tables schemas
DIM_ASSET_SCHEMA = sql.SQL("""
    CREATE TABLE IF NOT EXISTS dim_asset (
        asset_id INTEGER GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
        install_date DATE NOT NULL
    );
""")

DIM_ASSET_CATEGORY_SCHEMA = sql.SQL("""
    CREATE TABLE IF NOT EXISTS dim_asset_category (
        asset_category_id INTEGER GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
        category VARCHAR(50) NOT NULL UNIQUE
            CHECK (category IN ({values}))
    );
""").format(
    values=ASSET_CATEGORY_VALUES
)

DIM_TECHNICIAN_SCHEMA = sql.SQL("""
    CREATE TABLE IF NOT EXISTS dim_technician (
        technician_id INTEGER GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
        name VARCHAR(100) NOT NULL,
        specialty VARCHAR(50) NOT NULL
            CHECK (specialty IN ({values})),
        hire_date DATE NOT NULL
    );
""").format(
    values=ASSET_CATEGORY_VALUES
)

DIM_SITE_SCHEMA = sql.SQL("""
    CREATE TABLE IF NOT EXISTS dim_site (
        site_id INTEGER GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
        site_name VARCHAR(100) NOT NULL,
        address VARCHAR(200) NOT NULL,
        city VARCHAR(50) NOT NULL
    );
""")

DIM_FAILURE_MODE_SCHEMA = sql.SQL("""
    CREATE TABLE IF NOT EXISTS dim_failure_mode (
        failure_mode_id INTEGER GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
        name VARCHAR(50) NOT NULL UNIQUE
            CHECK (name IN ({values}))
    );
""").format(
    values=FAILURE_MODE_VALUES
)

# Link table schema
ASSET_CATEGORY_ASSIGNMENT_SCHEMA = sql.SQL("""
    CREATE TABLE IF NOT EXISTS asset_category_assignment (
        asset_id INTEGER NOT NULL
            REFERENCES dim_asset(asset_id),
        asset_category_id INTEGER NOT NULL
            REFERENCES dim_asset_category(asset_category_id),
        PRIMARY KEY (asset_id, asset_category_id)
    );
""")