from src.generators.failure_mode import generate_failure_modes
from src.validators.failure_mode import validate_failure_mode
from src.loaders.failure_mode import load_failure_mode
from src.db.connection import get_connection


def seed_failure_modes() -> None:
    """
    Generate, validate, and load the initial failure mode records.
    """
    failure_modes = generate_failure_modes()

    valid_rows = []

    for row in failure_modes:
        errors = validate_failure_mode(row)

        if errors:
            print(f"Invalid failure mode: {row}")

            for error in errors:
                print(f"- {error}")

            continue

        valid_rows.append(row)

    if len(valid_rows) != len(failure_modes):
        print("Failure mode seeding stopped because validation failed.")
        return

    try:
        with get_connection() as connection:
            for row in valid_rows:
                failure_mode_id = load_failure_mode(
                    row=row,
                    connection=connection,
                )

                print(
                    f"Loaded failure mode: "
                    f"{row['name']} (ID: {failure_mode_id})"
                )

    except Exception as exc:
        print(f"Failure mode seeding failed: {exc}")
        raise


if __name__ == "__main__":
    seed_failure_modes()