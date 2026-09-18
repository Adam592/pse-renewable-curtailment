import requests
import pandas as pd

BASE_URL = "https://api.raporty.pse.pl/api/"

def fetch_day(endpoint, date):
    parameters = {"$select": "rce_pln,dtime", "$filter": f"business_date eq '{date}'"}
    url = f"{BASE_URL}{endpoint}"
    try:
        response = requests.get(url, params=parameters)
        response.raise_for_status()
        data = response.json()
        return pd.DataFrame(data['value'])
    except requests.RequestException as e:
        print(f"Błąd dla {date}: {e}")
        return pd.DataFrame()

if __name__ == "__main__":
    result = fetch_day("rce-pln", "2025-06-14")
    print(result)