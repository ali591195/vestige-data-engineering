import math
from numbers import Real


FAILURE_MODES = (
    "TWF",
    "HDF",
    "PWF",
    "OSF",
    "RNF",
)

NUMERIC_FIELDS = (
    "air_temperature",
    "process_temperature",
    "rotational_speed",
    "torque",
    "tool_wear",
)


def validate_ai4i_row(row: dict) -> list[str]:
    """
    Validate one AI4I-style maintenance event before loading into Vestige.

    :param row: One AI4I-style maintenance event containing sensor data and
                its associated failure modes.
    :return: A list of validation errors. An empty list means the row is valid.
    """
    errors = []

    required_fields = (
        "air_temperature",
        "process_temperature",
        "rotational_speed",
        "torque",
        "tool_wear",
        "failure_modes",
    )

    for field in required_fields:
        if field not in row:
            errors.append(f"Missing required field: {field}")

    for field in NUMERIC_FIELDS:
        if field not in row:
            continue

        value = row[field]

        if isinstance(value, bool) or not isinstance(value, Real):
            errors.append(f"{field} must be numeric.")
            continue

        if not math.isfinite(value):
            errors.append(f"{field} must be finite.")
            continue

        if value < 0:
            errors.append(f"{field} cannot be negative.")

    if "failure_modes" in row:
        failure_modes = row["failure_modes"]

        if not isinstance(failure_modes, list):
            errors.append("failure_modes must be a list.")
        else:
            if not failure_modes:
                errors.append("failure_modes cannot be empty.")

            if len(failure_modes) != len(set(failure_modes)):
                errors.append("failure_modes cannot contain duplicates.")

            for failure_mode in failure_modes:
                if failure_mode not in FAILURE_MODES:
                    errors.append(
                        f"Invalid failure mode: {failure_mode}. "
                        f"Expected values from {FAILURE_MODES}."
                    )

    return errors


if __name__ == "__main__":
    from src.generators.ai4i import generate_failure_row

    row = generate_failure_row()

    row["failure_modes"] = [
        mode
        for mode in FAILURE_MODES
        if row[mode] == 1
    ]

    errors = validate_ai4i_row(row)

    if errors:
        print("Invalid AI4I row:")
        for error in errors:
            print(f"- {error}")
    else:
        print("Valid AI4I row:")
        print(row)