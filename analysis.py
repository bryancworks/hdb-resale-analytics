# import pandas as pd
# import matplotlib.pyplot as plt

def get_summary_snapshot(df):
    # Group avg prices for each Town
    avg_price_by_town = df.groupby("town", as_index=False)["resale_price"].mean().sort_values(by='resale_price', ascending=False)

    # Format cols
    avg_price_by_town.columns = ['Town', 'Avg Price (S$)']
    avg_price_by_town['Avg Price (S$)'] = avg_price_by_town['Avg Price (S$)'].round(0).astype(int)

    # Identify highest priced txn 
    top_txn = df.loc[df["resale_price"].idxmax()]

    return avg_price_by_town, top_txn

def get_town_ranking(df):
    return df["town"].value_counts().head(5)

def get_avg_prices_by_month_and_flat_type(df):
    avg_prices = df.groupby(['month', 'flat_type'])['resale_price'].mean().unstack().round(0).astype("Int64")   # still allows NaN values to be represented

    return avg_prices
