from pathlib import Path

import pandas as pd


RAW_DATA_PATH = Path("../../data/raw/ai4i2020.csv")
EXTRACTED_DATA_PATH = Path("../../data/extracted/ai4i_failures.csv")


def extract_failures() -> None:
    """
    Extract AI4I records representing machine failures and save them
    separately without modifying the original raw dataset.
    """

    if not RAW_DATA_PATH.exists():
        raise FileNotFoundError(f"Dataset not found: {RAW_DATA_PATH}")

    df = pd.read_csv(RAW_DATA_PATH)

    failures = df[df["Machine failure"] == 1].copy()

    EXTRACTED_DATA_PATH.parent.mkdir(parents=True, exist_ok=True)
    failures.to_csv(EXTRACTED_DATA_PATH, index=False)

    print(f"Extracted {len(failures)} failure records.")
    print(f"Saved to: {EXTRACTED_DATA_PATH}")


if __name__ == "__main__":
    extract_failures()