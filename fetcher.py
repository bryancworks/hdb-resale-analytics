import requests
import pandas as pd
import time
import logging
from datetime import datetime
from dateutil.relativedelta import relativedelta

logging.basicConfig(level=logging.INFO)

def fetch_hdb_data(months_back: int, api_key: str = None):
    # Fetch latest HDB resale flat transactions from data.gov.sg API
    url = "https://data.gov.sg/api/action/datastore_search"
    dataset_id = "d_8b84c4ee58e3cfc0ece0d773c8ca6abc"

    headers = {}
    if api_key:
        headers["x-api-key"] = api_key

    # Get list of recent months, e.g. ['2025-10', '2025-09', '2025-08']
    today = datetime.today()
    months = [(today - relativedelta(months=i)).strftime("%Y-%m") for i in range(months_back)]

    all_dfs = []

    fetched_months = []     # Track successfully fetched months for comparison with user selection in app.py

    start_time = time.time()
    for m in months:
        logging.info(f"Fetching data for month {m}...")
        
        params = {
            "resource_id": dataset_id,
            "limit": 3000,  # safe upper bound limit per month, since est. transactions per month ~2000+
            "filters": f'{{"month":"{m}"}}'
        }

        success = False

        for attempt in range(3):
            try:
                response = requests.get(url, params=params, headers=headers)

                if response.status_code == 200:
                    data = response.json()
                    success = True
                    break
                elif response.status_code == 429:
                    logging.warning(f"Rate limit hit for {m}. Retrying...")
                    time.sleep(2)
                else:
                    logging.error(f"Unexpected error {response.status_code} for {m}: {response.text}")
                    break

            except requests.exceptions.RequestException as e:
                logging.warning(f"Request exception for {m}: {e}")
                time.sleep(2)
        
        if not success:
            logging.warning(f"Skipping month {m} after retries")
            continue

        records = data["result"]["records"]

        if records:
            all_dfs.append(pd.DataFrame(records))
            fetched_months.append(m)
        
        time.sleep(1)  # avoid hitting rate limits

    if all_dfs:
        df = pd.concat(all_dfs, ignore_index=True)
        logging.info(f"✅ Successfully fetched total {len(df)} records over {months_back} months.")

        fetch_time_taken = time.time()-start_time
        logging.info("⌛ Time taken: %.2f seconds" % fetch_time_taken)
        return df, fetched_months
    else:
        logging.info("⚠️ No records fetched")
        return pd.DataFrame(), []
