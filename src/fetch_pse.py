import requests
import pandas as pd
import logging
from utils import save_raw, build_raw_filepath

BASE_URL = "https://api.raporty.pse.pl/api/"
DEFAULT_TIMEOUT = 30
DEFAULT_BATCH_SIZE = 100000

ENDPOINTS_CONFIG = {
    "rce-pln": {
        "start_date": "2024-07-01",
        "end_date": "2026-09-01"
    },
    "poze-redoze": {
        "start_date": "2024-10-01",
        "end_date": "2026-09-01"
    }
}

logger = logging.getLogger(__name__)

def fetch_info(endpoint: str, start_date: str, *,
                end_date: str | None=None, num_of_records: int = DEFAULT_BATCH_SIZE) -> pd.DataFrame:
    """The function fetches data from PSE API endpoint for a single day or a date range.
    Returns an empty DataFrame if fetch query failed."""

    if end_date is None:
        filter_str = f"business_date eq '{start_date}'"
    else:
        filter_str = f"business_date ge '{start_date}' and business_date le '{end_date}'"

    parameters = {
        "$filter": filter_str,
        "$first": num_of_records
    }
    url = f"{BASE_URL}{endpoint}"
    try:
        response = requests.get(url, params=parameters, timeout=DEFAULT_TIMEOUT)
        response.raise_for_status()
        data = response.json()
        df = pd.DataFrame(data['value'])
        logger.info(f"Successfully retrieved {len(df)} records.")
        return df
    except requests.RequestException as e:
        logger.error(f"An error occurred fetching the data: {e}" )
        return pd.DataFrame()

def main() -> None:
    """Fetches poze-redoze and rce-pln in required scope.
    Saves the data to data/raw"""

    for endpoint, config in ENDPOINTS_CONFIG.items():
        result = fetch_info(endpoint=endpoint, start_date=config["start_date"], end_date=config["end_date"], num_of_records=DEFAULT_BATCH_SIZE)
        filepath = build_raw_filepath(endpoint=endpoint, start_date=config["start_date"], end_date=config["end_date"])
        save_raw(result, filepath)
    
    return None

if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] %(message)s")
    main()