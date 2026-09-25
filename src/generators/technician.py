from datetime import date, timedelta
import random

from faker import Faker

from src.constants import ASSET_CATEGORIES

fake = Faker()

SPECIALTY_WEIGHTS = (
    0.34,
    0.63,
    0.02,
    0.01,
)


def generate_technician(specialty: str | None = None) -> dict:
    """
    Generate one synthetic technician record for Vestige.

    :param specialty: Optional technician specialty. If omitted, a specialty
                       is selected randomly according to the defined weights.
    :return: A dictionary containing a full name, specialty, and hire date.
    """
    if specialty is None:
        specialty = random.choices(
            population=ASSET_CATEGORIES,
            weights=SPECIALTY_WEIGHTS,
            k=1,
        )[0]
    elif specialty not in ASSET_CATEGORIES:
        raise ValueError(
            f"Invalid specialty: {specialty}. "
            f"Expected one of {ASSET_CATEGORIES}."
        )

    today = date.today()
    earliest_hire_date = today - timedelta(days=365)

    hire_date = fake.date_between(
        start_date=earliest_hire_date,
        end_date=today,
    )

    return {
        "name": fake.name(),
        "specialty": specialty,
        "hire_date": hire_date,
    }


if __name__ == "__main__":
    technician = generate_technician()
    print(technician)