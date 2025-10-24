import requests
import pandas as pd
import time
from datetime import datetime
from dateutil.relativedelta import relativedelta

# DEFAULT_LIMIT = 5000

def fetch_hdb_data(months_back=3):
    # Fetch latest HDB resale flat transactions from data.gov.sg API
    url = "https://data.gov.sg/api/action/datastore_search"
    dataset_id = "d_8b84c4ee58e3cfc0ece0d773c8ca6abc"

    # Get list of recent months, e.g. ['2025-10', '2025-09', '2025-08']
    today = datetime.today()
    months = [(today - relativedelta(months=i)).strftime("%Y-%m") for i in range(months_back)]

    all_dfs = []

    start_time = time.time()
    for m in months:
        # TODO: log instead of print
        print(f"Fetching data for month {m}...")
        params = {
            "resource_id": dataset_id,
            "limit": 5000,  # safe upper bound limit per month, since est. transactions per month ~2000+
            "filters": f'{{"month":"{m}"}}'
        }
        response = requests.get(url, params=params)
        response.raise_for_status()  # fail fast if API call fails
        data = response.json()

        records = data["result"]["records"]
        if records:
            all_dfs.append(pd.DataFrame(records))

    if all_dfs:
        df = pd.concat(all_dfs, ignore_index=True)
        print(f"✅ Successfully fetched total {len(df)} records over {months_back} months.")

        fetch_time_taken = time.time()-start_time
        print("⌛ Time taken: %.2f seconds" % fetch_time_taken)
        return df
    else:
        print("⚠️ No records fetched")
        return pd.DataFrame()
    