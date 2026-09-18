import requests
import pandas as pd
import logging

BASE_URL = "https://api.raporty.pse.pl/api/"
DEFAULT_TIMEOUT = 30
DEFAULT_BATCH_SIZE = 50000

logger = logging.getLogger(__name__)

def fetch_info(endpoint: str, start_date: str, select_params: str, *,
                end_date: str | None=None, num_of_records: int = DEFAULT_BATCH_SIZE) -> pd.DataFrame:
    """The function fetches data from PSE API endpoint for a single day or a date range.
    Returns an empty DataFrame if fetch query failed."""
    if end_date is None:
        filter_str = f"business_date eq '{start_date}'"
    else:
        filter_str = f"business_date ge '{start_date}' and business_date le '{end_date}'"

    parameters = {
        "$select": select_params,
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

    return None

if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] %(message)s")
    main()