from src.constants import FAILURE_MODES


def validate_failure_mode(row: dict) -> list[str]:
    """
    Validate one failure mode record before loading into Vestige.

    :param row: One failure mode record.
    :return: A list of validation errors. An empty list means the row is valid.
    """
    errors = []

    if "name" not in row:
        errors.append("Missing required field: name.")
    elif row["name"] not in FAILURE_MODES:
        errors.append(
            f"Invalid failure mode: {row['name']}. "
            f"Expected one of {FAILURE_MODES}."
        )

    return errors


if __name__ == "__main__":
    from src.generators.failure_mode import generate_failure_modes

    failure_mode = generate_failure_modes()[0]
    errors = validate_failure_mode(failure_mode)

    if errors:
        print("Invalid failure mode:")
        for error in errors:
            print(f"- {error}")
    else:
        print("Valid failure mode:")
        print(failure_mode)