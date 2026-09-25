from psycopg import sql

# Fact table schema
FACT_MAINTENANCE_EVENT_SCHEMA = sql.SQL("""
    CREATE TABLE IF NOT EXISTS fact_maintenance_event (
        event_id INTEGER GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
        asset_id INTEGER NOT NULL
            REFERENCES dim_asset(asset_id),
        site_id INTEGER NOT NULL
            REFERENCES dim_site(site_id),
        failure_date DATE NOT NULL,
        air_temperature DOUBLE PRECISION NOT NULL,
        process_temperature DOUBLE PRECISION NOT NULL,
        rotational_speed DOUBLE PRECISION NOT NULL,
        torque DOUBLE PRECISION NOT NULL,
        tool_wear DOUBLE PRECISION NOT NULL
    );
""")

# Link table schemas
MAINTENANCE_EVENT_TECHNICIAN_SCHEMA = sql.SQL("""
    CREATE TABLE IF NOT EXISTS maintenance_event_technician (
        event_id INTEGER NOT NULL
            REFERENCES fact_maintenance_event(event_id),
        technician_id INTEGER NOT NULL
            REFERENCES dim_technician(technician_id),
        PRIMARY KEY (event_id, technician_id)
    );
""")

MAINTENANCE_EVENT_FAILURE_MODE_SCHEMA = sql.SQL("""
    CREATE TABLE IF NOT EXISTS maintenance_event_failure_mode (
        event_id INTEGER NOT NULL
            REFERENCES fact_maintenance_event(event_id),
        failure_mode_id INTEGER NOT NULL
            REFERENCES dim_failure_mode(failure_mode_id),
        PRIMARY KEY (event_id, failure_mode_id)
    );
""")