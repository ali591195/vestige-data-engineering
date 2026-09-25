from pathlib import Path

import pandas as pd


DATA_PATH = Path("../../data/raw/ai4i2020.csv")


def inspect_dataset() -> None:
    """
    Inspect the AI4I 2020 dataset without modifying it.
    """
    if not DATA_PATH.exists():
        raise FileNotFoundError(f"Dataset not found: {DATA_PATH}")

    df = pd.read_csv(DATA_PATH)

    print("=== FILE ===")
    print(DATA_PATH)

    print("\n=== MISSING VALUES ===")
    print(df.isna().sum())

    print("\n=== DUPLICATE ROWS ===")
    print(df.duplicated().sum())

    failures = df[df["Machine failure"] == 1]

    print("\n=== FAILURE COUNT ===")
    print(len(failures))

    print("\n=== FIRST 5 ROWS ===")
    print(df.head())


if __name__ == "__main__":
    inspect_dataset()