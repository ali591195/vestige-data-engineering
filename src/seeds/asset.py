from src.generators.asset import generate_asset
from src.validators.asset import validate_asset
from src.loaders.asset import load_asset
from src.db.connection import get_connection


def seed_assets(asset_count: int = 206) -> None:
    """
    Generate, validate, and load the initial asset records.

    :param asset_count: Number of assets to generate and load.
    """
    assets = [generate_asset() for _ in range(asset_count)]

    valid_rows = []

    for row in assets:
        errors = validate_asset(row)

        if errors:
            print(f"Invalid asset: {row}")

            for error in errors:
                print(f"- {error}")

            continue

        valid_rows.append(row)

    if not valid_rows:
        print("No valid assets to load.")
        return

    try:
        with get_connection() as connection:
            for row in valid_rows:
                asset_id = load_asset(
                    row=row,
                    connection=connection,
                )

                print(
                    f"Loaded asset: "
                    f"{row['asset_category']} (ID: {asset_id})"
                )

    except Exception as exc:
        print(f"Asset seeding failed: {exc}")
        raise


if __name__ == "__main__":
    seed_assets()