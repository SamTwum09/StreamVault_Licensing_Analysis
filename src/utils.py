import pandas as pd


def coerce_boolean_franchise(series: pd.Series) -> pd.Series:
    """Consistently coerce is_franchise column to boolean Series across scripts."""
    if series.dtype == bool:
        return series
    return series.astype(str).str.strip().str.lower().isin(["true", "1"])
