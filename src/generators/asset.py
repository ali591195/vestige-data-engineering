from datetime import date, timedelta
import random

from src.constants import ASSET_CATEGORIES


CATEGORY_WEIGHTS = (
    0.40,
    0.40,
    0.15,
    0.05,
)

ADDITIONAL_CATEGORY_PROBABILITIES = (
    0.10,
    0.02,
    0.002,
)


def generate_asset() -> dict:
    """
    Generate one synthetic asset record for Vestige.
    """

    today = date.today()
    earliest_install_date = today - timedelta(days=365)

    days = (today - earliest_install_date).days

    install_date = earliest_install_date + timedelta(
        days=random.randint(0, days),
    )

    remaining_categories = list(ASSET_CATEGORIES)
    remaining_weights = list(CATEGORY_WEIGHTS)

    categories = []

    first_category = random.choices(
        population=remaining_categories,
        weights=remaining_weights,
        k=1,
    )[0]
    categories.append(first_category)

    selected_index = remaining_categories.index(first_category)
    remaining_categories.pop(selected_index)
    remaining_weights.pop(selected_index)

    for probability in ADDITIONAL_CATEGORY_PROBABILITIES:
        if not remaining_categories or random.random() >= probability:
            break

        category = random.choices(
            population=remaining_categories,
            weights=remaining_weights,
            k=1,
        )[0]
        categories.append(category)

        selected_index = remaining_categories.index(category)
        remaining_categories.pop(selected_index)
        remaining_weights.pop(selected_index)

    return {
        "asset_category": categories,
        "install_date": install_date,
    }

if __name__ == "__main__":
    asset = generate_asset()
    print(asset)