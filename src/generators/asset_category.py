from src.constants import ASSET_CATEGORIES


def generate_asset_categories() -> list[dict]:
    """
    Generate the four synthetic asset category records for Vestige.
    """
    return [
        {
            "category": category,
        }
        for category in ASSET_CATEGORIES
    ]


if __name__ == "__main__":
    asset_categories = generate_asset_categories()

    for asset_category in asset_categories:
        print(asset_category)