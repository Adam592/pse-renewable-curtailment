import pandas as pd
from pathlib import Path
import logging

logger = logging.getLogger(__name__)


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
