from src.generators.asset_category import generate_asset_categories
from src.validators.asset_category import validate_asset_category
from src.loaders.asset_category import load_asset_category
from src.db.connection import get_connection


def seed_asset_categories() -> None:
    """
    Generate, validate, and load the initial asset category records.
    """
    asset_categories = generate_asset_categories()

    valid_rows = []

    for row in asset_categories:
        errors = validate_asset_category(row)

        if errors:
            print(f"Invalid asset category: {row}")

            for error in errors:
                print(f"- {error}")

            continue

        valid_rows.append(row)

    if len(valid_rows) != len(asset_categories):
        print("Asset category seeding stopped because validation failed.")
        return

    try:
        with get_connection() as connection:
            for row in valid_rows:
                asset_category_id = load_asset_category(
                    row=row,
                    connection=connection,
                )

                print(
                    f"Loaded asset category: "
                    f"{row['category']} (ID: {asset_category_id})"
                )

    except Exception as exc:
        print(f"Asset category seeding failed: {exc}")
        raise


if __name__ == "__main__":
    seed_asset_categories()