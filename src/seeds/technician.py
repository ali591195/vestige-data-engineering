from src.generators.technician import generate_technician
from src.validators.technician import validate_technician
from src.loaders.technician import load_technician
from src.db.connection import get_connection


def seed_technicians(
    technician_count: int = 20,
    specialties: list[str] | None = None,
) -> None:
    """
    Generate, validate, and load the initial technician records.

    :param technician_count: Number of technicians to generate and load.
    :param specialties: Optional list of specialties to assign to technicians.
    """
    if specialties is not None and len(specialties) != technician_count:
        raise ValueError(
            "The number of specialties must match technician_count."
        )

    if specialties is None:
        technicians = [
            generate_technician()
            for _ in range(technician_count)
        ]
    else:
        technicians = [
            generate_technician(specialty=specialty)
            for specialty in specialties
        ]

    valid_rows = []

    for row in technicians:
        errors = validate_technician(row)

        if errors:
            print(f"Invalid technician: {row}")

            for error in errors:
                print(f"- {error}")

            continue

        valid_rows.append(row)

    if not valid_rows:
        print("No valid technicians to load.")
        return

    try:
        with get_connection() as connection:
            for row in valid_rows:
                technician_id = load_technician(
                    row=row,
                    connection=connection,
                )

                print(
                    f"Loaded technician: "
                    f"{row['name']} (ID: {technician_id})"
                )

    except Exception as exc:
        print(f"Technician seeding failed: {exc}")
        raise


if __name__ == "__main__":
    seed_technicians()