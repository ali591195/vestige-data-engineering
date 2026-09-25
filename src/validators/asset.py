from datetime import date

from src.constants import ASSET_CATEGORIES


def validate_asset(row: dict) -> list[str]:
    """
    Validate one synthetic asset record before loading into Vestige.

    :param row: One asset record containing asset categories and install date.
    :return: A list of validation errors. An empty list means the row is valid.
    """
    errors = []

    required_fields = (
        "asset_category",
        "install_date",
    )

    for field in required_fields:
        if field not in row:
            errors.append(f"Missing required field: {field}")

    if "asset_category" in row:
        categories = row["asset_category"]

        if not isinstance(categories, list):
            errors.append("asset_category must be a list.")
        else:
            if not categories:
                errors.append("asset_category cannot be empty.")

            if len(categories) != len(set(categories)):
                errors.append("asset_category cannot contain duplicates.")

            for category in categories:
                if category not in ASSET_CATEGORIES:
                    errors.append(
                        f"Invalid asset category: {category}. "
                        f"Expected values from {ASSET_CATEGORIES}."
                    )

    if "install_date" in row:
        install_date = row["install_date"]

        if not isinstance(install_date, date):
            errors.append("install_date must be a date.")
        elif install_date > date.today():
            errors.append("install_date cannot be in the future.")

    return errors


if __name__ == "__main__":
    from src.generators.asset import generate_asset

    asset = generate_asset()
    errors = validate_asset(asset)

    if errors:
        print("Invalid asset:")
        for error in errors:
            print(f"- {error}")
    else:
        print("Valid asset:")
        print(asset)