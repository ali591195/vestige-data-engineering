from psycopg import sql

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
            CHECK (
                category IN (
                    'HVAC',
                    'ELECTRICAL',
                    'VERTICAL_TRANSPORTATION',
                    'HOISTING'
                )
            )
    );
""")

DIM_TECHNICIAN_SCHEMA = sql.SQL("""
    CREATE TABLE IF NOT EXISTS dim_technician (
        technician_id INTEGER GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
        name VARCHAR(100) NOT NULL,
        specialty VARCHAR(50) NOT NULL
            CHECK (
                specialty IN (
                    'HVAC',
                    'ELECTRICAL',
                    'VERTICAL_TRANSPORTATION',
                    'HOISTING'
                )
            ),
        hire_date DATE NOT NULL
    );
""")

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
            CHECK (
                name IN (
                    'TOOL_WEAR_FAILURE',
                    'HEAT_DISSIPATION_FAILURE',
                    'POWER_FAILURE',
                    'OVERSTRAIN_FAILURE',
                    'RANDOM_FAILURE'
                )
            )
    );
""")

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