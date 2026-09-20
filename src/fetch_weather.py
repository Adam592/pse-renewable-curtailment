import requests
import pandas as pd
import logging
from utils import save_raw, build_raw_filepath

BASE_URL = "https://archive-api.open-meteo.com/v1/archive"
DEFAULT_TIMEOUT = 30
PARAMS_CONFIG = {
    "latitude": 51.9194,
    "longitude": 19.1451,
    "start_date": "2024-10-01",
    "end_date": "2026-09-01",
    "time_interval": "hourly",
    "select_params": "wind_speed_10m,shortwave_radiation"
}

logger = logging.getLogger(__name__)

def fetch_weather(latitude: float, longitude: float, start_date: str, end_date: str, time_interval: str, select_params: str) -> pd.DataFrame:
    """The function fetches data from Open-Meteo API when given latitude, longitude, 
    desired time intervals (eg. 15 minutes, 1 hour) and parameters to return"""

    parameters = {
        "latitude": latitude,
        "longitude": longitude,
        "start_date": start_date,
        "end_date": end_date,
        time_interval: select_params,
    }

    try:
        response = requests.get(BASE_URL, params=parameters, timeout=DEFAULT_TIMEOUT)
        response.raise_for_status()
        data = response.json()
        df = pd.DataFrame(data[time_interval])
        logger.info(f"Successfully retrieved {len(df)} records.")
        return df
    except requests.RequestException as e:
        logger.error(f"An error occurred fetching the data: {e}" )
        if e.response is not None:
            logger.error(f"Response body: {e.response.text}")
        return pd.DataFrame()

def main():
    """Fetches data from Open-Meteo API in required scope.
      Saves the data to data/raw."""

    result = fetch_weather(PARAMS_CONFIG["latitude"], PARAMS_CONFIG['longitude'], PARAMS_CONFIG["start_date"], PARAMS_CONFIG["end_date"], PARAMS_CONFIG["time_interval"], PARAMS_CONFIG["select_params"])
    filepath = build_raw_filepath("weather", PARAMS_CONFIG["start_date"], end_date=PARAMS_CONFIG["end_date"])
    save_raw(result, filepath)

if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] %(message)s")
    main()