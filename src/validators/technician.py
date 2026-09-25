from datetime import date

from src.constants import ASSET_CATEGORIES


def validate_technician(row: dict) -> list[str]:
    """
    Validate one synthetic technician record before loading into Vestige.

    :param row: One synthetic technician record.
    :return: A list of validation errors. An empty list means the row is valid.
    """
    errors = []

    required_fields = (
        "name",
        "specialty",
        "hire_date",
    )

    for field in required_fields:
        if field not in row:
            errors.append(f"Missing required field: {field}.")
        elif field in ("name", "specialty") and not isinstance(row[field], str):
            errors.append(f"{field} must be a string.")
        elif field in ("name", "specialty") and not row[field].strip():
            errors.append(f"{field} cannot be empty.")

    if "specialty" in row:
        if row["specialty"] not in ASSET_CATEGORIES:
            errors.append(
                f"Invalid specialty: {row['specialty']}. "
                f"Expected one of {ASSET_CATEGORIES}."
            )

    if "hire_date" in row:
        if not isinstance(row["hire_date"], date):
            errors.append("hire_date must be a date.")
        elif row["hire_date"] > date.today():
            errors.append("hire_date cannot be in the future.")

    return errors


if __name__ == "__main__":
    from src.generators.technician import generate_technician

    technician = generate_technician()
    errors = validate_technician(technician)

    if errors:
        print("Invalid technician:")
        for error in errors:
            print(f"- {error}")
    else:
        print("Valid technician:")
        print(technician)