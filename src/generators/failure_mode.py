from src.constants import FAILURE_MODES


def generate_failure_modes() -> list[dict]:
    """
    Generate the five AI4I failure mode records for Vestige.
    """
    return [
        {
            "name": failure_mode,
        }
        for failure_mode in FAILURE_MODES
    ]


if __name__ == "__main__":
    failure_modes = generate_failure_modes()

    for failure_mode in failure_modes:
        print(failure_mode)