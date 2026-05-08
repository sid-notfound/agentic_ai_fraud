from pathlib import Path

import pandas as pd


def load_transactions(csv_path: str | Path) -> pd.DataFrame:
    df = pd.read_csv(csv_path)
    df["timestamp"] = pd.to_datetime(df["timestamp"], utc=False)
    return df

