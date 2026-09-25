import math
import random


FAILURE_MODES = ("TWF", "HDF", "PWF", "OSF", "RNF")

OSF_THRESHOLDS = {
    "L": 11000,
    "M": 12000,
    "H": 13000,
}


def generate_failure_row(
    target_mode: str | None = None,
    product_type: str | None = None,
) -> dict:
    """
    Generate one AI4I-style failure record containing the sensor measurements
    and failure-mode indicators required by Vestige.

    :param target_mode: Optional failure mode that the generated record must
                        trigger. If omitted, a failure mode is selected randomly.
    :param product_type: Optional AI4I product type (L, M, or H).
    :return: A dictionary containing the product type, sensor measurements,
             and five failure-mode indicators.
    """

    if target_mode is None:
        target_mode = random.choice(FAILURE_MODES)
    elif target_mode not in FAILURE_MODES:
        raise ValueError(
            f"Invalid failure mode: {target_mode}. "
            f"Expected one of {FAILURE_MODES}."
        )

    if product_type is None:
        product_type = random.choices(
            population=["L", "M", "H"],
            weights=[0.50, 0.30, 0.20],
            k=1,
        )[0]
    elif product_type not in {"L", "M", "H"}:
        raise ValueError("product_type must be 'L', 'M', or 'H'.")

    # Base sensor values following the documented AI4I relationships.
    air_temperature = round(random.gauss(300, 2), 1)
    process_temperature = round(
        air_temperature + random.gauss(10, 1),
        1,
    )

    torque = max(0.1, round(random.gauss(40, 10), 1))

    # AI4I derives rotational speed from approximately 2860 W of power.
    rotational_speed = round(
        (2860 * 60) / (2 * math.pi * torque)
    )

    tool_wear = random.randint(0, 199)

    # Force the requested failure condition.
    if target_mode == "TWF":
        tool_wear = random.randint(200, 240)

    elif target_mode == "HDF":
        process_temperature = round(
            air_temperature + random.uniform(7.5, 8.5),
            1,
        )
        rotational_speed = random.randint(1200, 1370)

    elif target_mode == "PWF":
        torque = round(random.uniform(25, 30), 1)
        rotational_speed = random.randint(800, 1000)

    elif target_mode == "OSF":
        tool_wear = random.randint(220, 240)
        torque = round(random.uniform(60, 70), 1)

    # Evaluate all five independent failure modes.
    temperature_difference = process_temperature - air_temperature
    power = torque * rotational_speed * (2 * math.pi / 60)
    wear_torque = tool_wear * torque

    failures = {
        "TWF": 200 <= tool_wear <= 240,
        "HDF": (
            temperature_difference < 8.6
            and rotational_speed < 1380
        ),
        "PWF": (
            power < 3500
            or power > 9000
        ),
        "OSF": wear_torque > OSF_THRESHOLDS[product_type],
        "RNF": random.random() < 0.001,
    }

    # Guarantee the selected failure mode.
    failures[target_mode] = True

    return {
        "type": product_type,
        "air_temperature": air_temperature,
        "process_temperature": process_temperature,
        "rotational_speed": rotational_speed,
        "torque": torque,
        "tool_wear": tool_wear,
        "TWF": int(failures["TWF"]),
        "HDF": int(failures["HDF"]),
        "PWF": int(failures["PWF"]),
        "OSF": int(failures["OSF"]),
        "RNF": int(failures["RNF"]),
    }


if __name__ == "__main__":
    row = generate_failure_row()
    print(row)