import pandas as pd
import matplotlib.pyplot as plt

def show_summary_snapshot(df):
    # Group avg prices for each Town
    avg_price_by_town = df.groupby("town", as_index=False)["resale_price"].mean().sort_values(by='resale_price', ascending=False)

    # Format cols
    avg_price_by_town.columns = ['Town', 'Price (S$)']
    avg_price_by_town['Price (S$)'] = avg_price_by_town['Price (S$)'].round(0).astype(int)

    print("\n🏙️ Average Resale Price per Town:")
    print(avg_price_by_town.to_string(index=False))

    # Identify highest priced txn 
    top_txn = df.loc[df["resale_price"].idxmax()]

    print("\n💰 Highest Priced Transaction:")
    print(f"{top_txn['town']} — S${int(top_txn['resale_price']):,} "
          f"({top_txn['flat_type']}, {top_txn['month']})")

def show_town_ranking(df):
    ranking = df["town"].value_counts().head(5)
    print("\n🏆 Top 5 Towns by Number of Transactions:")
    for i, (town, count) in enumerate(ranking.items(), start=1):
        print(f"{i}. {town} — {count} transactions")

def plot_price_comparison_chart(df):
    avg_prices = df.groupby(['month', 'flat_type'])['resale_price'].mean().unstack()
    
    # Plot chart
    avg_prices.plot(kind="bar", figsize=(10,6))
    
    plt.title("Average Resale Price by Flat Type")
    plt.ylabel("Price (S$)")
    plt.xlabel('Month')
    plt.xticks(rotation=0)
    plt.legend(title="Flat Type")
    plt.tight_layout()
    plt.show()
