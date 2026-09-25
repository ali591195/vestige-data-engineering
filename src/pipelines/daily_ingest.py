import random

from src.generators.ai4i import generate_failure_row
from src.validators.ai4i import validate_ai4i
from src.loaders.fact import load_fact
from src.db.connection import get_connection


FACT_ROW_LIMIT = 10_000

FAILURE_MODE_COLUMNS = {
    "TWF": "TOOL_WEAR_FAILURE",
    "HDF": "HEAT_DISSIPATION_FAILURE",
    "PWF": "POWER_FAILURE",
    "OSF": "OVERSTRAIN_FAILURE",
    "RNF": "RANDOM_FAILURE",
}


def get_batch_size() -> int:
    """
    Select a daily batch size from 1 to 5.
    Larger batches are progressively less common.
    """
    return random.choices(
        [1, 2, 3, 4, 5],
        weights=[30, 25, 20, 15, 10],
        k=1,
    )[0]


def prepare_row(source_row: dict) -> dict:
    """
    Convert one generated AI4I-style record into the structure
    expected by the Vestige validator and fact loader.
    """
    failure_modes = [
        failure_mode
        for source_column, failure_mode in FAILURE_MODE_COLUMNS.items()
        if source_row[source_column] == 1
    ]

    return {
        "air_temperature": source_row["air_temperature"],
        "process_temperature": source_row["process_temperature"],
        "rotational_speed": source_row["rotational_speed"],
        "torque": source_row["torque"],
        "tool_wear": source_row["tool_wear"],
        "failure_modes": failure_modes,
    }


def daily_ingest() -> None:
    """
    Generate, validate, and load a random daily batch of AI4I-style
    maintenance events while respecting the project fact-row limit.
    """
    batch_size = get_batch_size()

    try:
        with get_connection() as connection:
            with connection.cursor() as cursor:
                cursor.execute(
                    """
                    SELECT COUNT(*)
                    FROM fact_maintenance_event;
                    """
                )

                current_count = cursor.fetchone()[0]

            if current_count + batch_size > FACT_ROW_LIMIT:
                print(
                    f"Fact row limit reached. "
                    f"Current rows: {current_count}, "
                    f"requested batch: {batch_size}, "
                    f"limit: {FACT_ROW_LIMIT}."
                )
                return

            rows = [
                prepare_row(generate_failure_row())
                for _ in range(batch_size)
            ]

            valid_rows = []

            for row in rows:
                errors = validate_ai4i(row)

                if errors:
                    print(f"Invalid AI4I event: {row}")

                    for error in errors:
                        print(f"- {error}")

                    continue

                valid_rows.append(row)

            if not valid_rows:
                print("No valid AI4I events to load.")
                return

            for row in valid_rows:
                event_id = load_fact(
                    row=row,
                    connection=connection,
                )

                print(
                    f"Loaded AI4I event "
                    f"(ID: {event_id}, "
                    f"failure modes: {row['failure_modes']})"
                )

    except Exception as exc:
        print(f"Daily ingestion failed: {exc}")
        raise


if __name__ == "__main__":
    daily_ingest()