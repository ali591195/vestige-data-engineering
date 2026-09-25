from src.generators.site import generate_site
from src.validators.site import validate_site
from src.loaders.site import load_site
from src.db.connection import get_connection


def seed_sites(site_count: int = 120) -> None:
    """
    Generate, validate, and load the initial site records.

    :param site_count: Number of sites to generate and load.
    """
    sites = [generate_site() for _ in range(site_count)]

    valid_rows = []

    for row in sites:
        errors = validate_site(row)

        if errors:
            print(f"Invalid site: {row}")

            for error in errors:
                print(f"- {error}")

            continue

        valid_rows.append(row)

    if not valid_rows:
        print("No valid sites to load.")
        return

    try:
        with get_connection() as connection:
            for row in valid_rows:
                site_id = load_site(
                    row=row,
                    connection=connection,
                )

                print(
                    f"Loaded site: "
                    f"{row['site_name']} (ID: {site_id})"
                )

    except Exception as exc:
        print(f"Site seeding failed: {exc}")
        raise


if __name__ == "__main__":
    seed_sites()