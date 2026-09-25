import random

from faker import Faker

fake = Faker()

LAHORE_AREAS = (
    "GULBERG",
    "MODEL_TOWN",
    "JOHAR_TOWN",
    "GARDEN_TOWN",
    "FAISAL_TOWN",
    "DHA",
    "WAPDA_TOWN",
    "TOWNSHIP",
)

AREA_WEIGHTS = (
    0.25,
    0.20,
    0.15,
    0.12,
    0.10,
    0.08,
    0.05,
    0.05,
)

SITE_NAME_TEMPLATES = (
    "{name} Residence",
    "{name} House",
    "{name} Family Residence",
    "{company} Office",
    "{company} Warehouse",
    "{company} Commercial Building",
    "{company} Technical Services",
)


def generate_site(area: str | None = None) -> dict:
    """
    Generate one synthetic site record for Vestige.

    :param area: Optional Lahore area. If omitted, an area is selected
                 randomly according to the defined weights.
    :return: A dictionary containing a site name, address, and city.
    """
    if area is None:
        area = random.choices(
            population=LAHORE_AREAS,
            weights=AREA_WEIGHTS,
            k=1,
        )[0]
    elif area not in LAHORE_AREAS:
        raise ValueError(
            f"Invalid area: {area}. "
            f"Expected one of {LAHORE_AREAS}."
        )

    name = fake.name()
    company = fake.company()

    site_name_template = random.choice(SITE_NAME_TEMPLATES)

    if "{name}" in site_name_template:
        site_name = site_name_template.format(name=name)
    else:
        site_name = site_name_template.format(company=company)

    house_number = random.randint(1, 250)
    street_number = random.randint(1, 30)
    block = random.choice(("A", "B", "C", "D", "E"))

    address = (
        f"House {house_number}, Street {street_number}, "
        f"Block {block}, {area.replace('_', ' ').title()}, Lahore"
    )

    return {
        "site_name": site_name,
        "address": address,
        "city": "Lahore",
    }


if __name__ == "__main__":
    site = generate_site()
    print(site)
