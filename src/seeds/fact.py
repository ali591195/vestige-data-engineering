from pathlib import Path

import pandas as pd

from src.constants import FAILURE_MODES
from src.validators.ai4i import validate_ai4i
from src.loaders.fact import load_fact
from src.db.connection import get_connection


EXTRACTED_DATA_PATH = (
    Path(__file__).resolve().parents[2]
    / "data"
    / "extracted"
    / "ai4i_failures.csv"
)

FAILURE_MODE_COLUMNS = {
    "TWF": "TOOL_WEAR_FAILURE",
    "HDF": "HEAT_DISSIPATION_FAILURE",
    "PWF": "POWER_FAILURE",
    "OSF": "OVERSTRAIN_FAILURE",
    "RNF": "RANDOM_FAILURE",
}


def seed_ai4i() -> None:
    """
    Prepare, validate, and load AI4I failure records from the
    extracted CSV.
    """

    if not EXTRACTED_DATA_PATH.exists():
        raise FileNotFoundError(
            f"Extracted AI4I dataset not found: {EXTRACTED_DATA_PATH}"
        )

    df = pd.read_csv(EXTRACTED_DATA_PATH)

    rows = []

    for _, source_row in df.iterrows():
        failure_modes = [
            failure_mode
            for source_column, failure_mode in FAILURE_MODE_COLUMNS.items()
            if source_row[source_column] == 1
        ]

        row = {
            "air_temperature": source_row["Air temperature [K]"],
            "process_temperature": source_row["Process temperature [K]"],
            "rotational_speed": source_row["Rotational speed [rpm]"],
            "torque": source_row["Torque [Nm]"],
            "tool_wear": source_row["Tool wear [min]"],
            "failure_modes": failure_modes,
        }

        rows.append(row)

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

    try:
        with get_connection() as connection:
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
        print(f"AI4I seeding failed: {exc}")
        raise


if __name__ == "__main__":
    seed_ai4i()