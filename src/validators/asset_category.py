from src.constants import ASSET_CATEGORIES


def validate_asset_category(row: dict) -> list[str]:
    """
    Validate one synthetic asset category record before loading into Vestige.

    :param row: One asset category record.
    :return: A list of validation errors. An empty list means the row is valid.
    """
    errors = []

    if "category" not in row:
        errors.append("Missing required field: category.")
    elif row["category"] not in ASSET_CATEGORIES:
        errors.append(
            f"Invalid asset category: {row['category']}. "
            f"Expected one of {ASSET_CATEGORIES}."
        )

    return errors


if __name__ == "__main__":
    from src.generators.asset_category import generate_asset_categories

    asset_category = generate_asset_categories()[0]
    errors = validate_asset_category(asset_category)

    if errors:
        print("Invalid asset category:")
        for error in errors:
            print(f"- {error}")
    else:
        print("Valid asset category:")
        print(asset_category)