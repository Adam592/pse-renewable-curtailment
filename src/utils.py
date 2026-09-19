import pandas as pd
from pathlib import Path
import logging

logger = logging.getLogger(__name__)
RAW_DATA_DIR = Path("../data/raw")

def save_raw(df :pd.DataFrame, filepath: Path) -> None:
    """The function given a dataframe saves it as a Parquet file to preselected filepath."""

    try:
        if df.empty:
            logger.warning("Unable to save an empty dataframe to a file")
        else:
            filepath.parent.mkdir(parents=True, exist_ok=True)
            df.to_parquet(filepath, engine="pyarrow", compression="snappy")
            logger.info(f"Successfully saved {len(df)} records to {filepath}")
    except Exception as e:
        logger.error(f"An error occurred saving the data: {e}")

def build_raw_filepath(endpoint: str, start_date: str, *, end_date: str | None=None):
    """Builds a filepath for raw data based on endpoint and dates given"""

    if end_date is None:
        return RAW_DATA_DIR / f"{endpoint}_{start_date}.parquet"
    else:
        return RAW_DATA_DIR / f"{endpoint}_{start_date}_to_{end_date}.parquet"