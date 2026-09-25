from pathlib import Path
from utils import load_raw, build_raw_filepath, save_raw
import pandas as pd
import logging

logger = logging.getLogger(__name__)

def format_dtime(df: pd.DataFrame) -> pd.DataFrame:
    df["dtime_utc"] = pd.to_datetime(df["dtime_utc"], utc=True)
    df["dtime_local"] = df["dtime_utc"].dt.tz_convert("Europe/Warsaw")
    df = df.drop(columns=["period_utc", "dtime"])
    df = df.astype({'period': 'string',
        'business_date': 'datetime64[ns]',
        'publication_ts_utc': 'datetime64[ns, UTC]',
        'publication_ts': 'datetime64[ns]'})
    
    cols = ["publication_ts", "publication_ts_utc"]
    df[cols] = df[cols].apply(lambda col: col.dt.floor("s"))
    return df

def transform_weather(df: pd.DataFrame) -> pd.DataFrame:
    """ """

    df["dtime_utc"] = pd.to_datetime(df["time"], utc=True)
    df["dtime_local"] = df["dtime_utc"].dt.tz_convert("Europe/Warsaw")
    df = df.drop(columns=["time"])
    df = df[df["dtime_local"] >= "2024-10-01"]

    df = df.set_index("dtime_utc")
    df = df.resample("15min").bfill()
    df = df.reset_index()

    df["dtime_utc"] = df["dtime_utc"] + pd.Timedelta(minutes=15)
    df["dtime_local"] = df["dtime_local"] + pd.Timedelta(minutes=15)

    df = df[["dtime_utc", "dtime_local", "wind_speed_10m", "shortwave_radiation"]]

    return df

def transform_rce_pln(df: pd.DataFrame) -> pd.DataFrame:
    """ """

    df = format_dtime(df)
    df = df[["dtime_utc", "dtime_local", "period", "rce_pln", "business_date", "publication_ts_utc", "publication_ts"]]

    return df

def transform_poze_redoze(df: pd.DataFrame) -> pd.DataFrame:
    """ """

    df = format_dtime(df)
    df = df.fillna(0)
    df = df[["dtime_utc", "dtime_local", "period", "pv_red_balance", "pv_red_network", "wi_red_balance", "wi_red_network", "business_date", "publication_ts_utc", "publication_ts"]]

    mw_cols = ["pv_red_balance", "pv_red_network", "wi_red_balance", "wi_red_network"]
    for col in mw_cols:
        df[f"{col}_mwh"] = df[col] * 0.25

    return df

def main() -> None:
    """ """

    rce_pln = load_raw(build_raw_filepath("rce-pln", "2024-07-01", end_date="2026-09-01"))
    poze_redoze = load_raw(build_raw_filepath("poze-redoze", "2024-10-01", end_date="2026-09-01"))
    weather = load_raw(build_raw_filepath("weather", "2024-09-30", end_date="2026-09-01"))

    rce_pln = transform_rce_pln(rce_pln)
    rce_pln.to_parquet("../data/processed/pr-rce-pln.parquet")

    poze_redoze = transform_poze_redoze(poze_redoze)
    poze_redoze.to_parquet("../data/processed/pr-poze-redoze.parquet")

    weather = transform_weather(weather)
    weather.to_parquet("../data/processed/pr-weather.parquet")


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] %(message)s")
    main()


