def validate_site(row: dict) -> list[str]:
    """
    Validate one synthetic site record before loading into Vestige.

    :param row: One synthetic site record.
    :return: A list of validation errors. An empty list means the row is valid.
    """
    errors = []

    required_fields = (
        "site_name",
        "address",
        "city",
    )

    for field in required_fields:
        if field not in row:
            errors.append(f"Missing required field: {field}.")
        elif not isinstance(row[field], str):
            errors.append(f"{field} must be a string.")
        elif not row[field].strip():
            errors.append(f"{field} cannot be empty.")

    return errors


if __name__ == "__main__":
    from src.generators.site import generate_site

    site = generate_site()
    errors = validate_site(site)

    if errors:
        print("Invalid site:")
        for error in errors:
            print(f"- {error}")
    else:
        print("Valid site:")
        print(site)