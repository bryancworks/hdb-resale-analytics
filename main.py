import sys
import pandas as pd
import argparse
from fetcher import fetch_hdb_data
from analysis import (show_summary_snapshot, show_town_ranking, plot_price_comparison_chart)

def validate_months(months):
    months_intval = int(months)
    if months_intval < 1 or months_intval > 5:
        raise argparse.ArgumentTypeError("Number of months must be between 1 and 5.")
    return months_intval 

def main():
    parser = argparse.ArgumentParser(description="HDB Resale Data Analytics")
    parser.add_argument('--months', 
                        type=validate_months, 
                        default=3, 
                        help="Number of months to fetch (1-5). Default is 3.")
    args = parser.parse_args()

    print("📊 Welcome to the HDB Resale Data Analytics!")

    # Fetch data
    print(f"\nFetching last {args.months} months of HDB resale data...")
    df = fetch_hdb_data(args.months)
    
    # Since no data fetched, no analysis to be done, exit program
    if df.empty:
        print("❌ No data fetched. Exiting program.")
        sys.exit(0)

    # Convert resale prices to numeric data type
    df['resale_price'] = pd.to_numeric(df['resale_price'], errors='coerce') # coerce prevents exception being raised and halting program

    # Interactive menu loop
    while True:
        print("\n=== Main Menu ===")
        print("1. Apply filters")
        print("2. View summary snapshot")
        print("3. View town ranking")
        print("4. Chart comparison")
        print("5. Exit")

        choice = input("\nEnter your choice: ").strip()

        if choice == "1":
            filtered_df = apply_filters(df)

            if filtered_df.empty:
                print("❌ No records found with filters. Please try again.")
                continue

            # Format dataset
            formatted_df = filtered_df.rename(
                columns={'month': 'Month',
                         'town': 'Town',
                         'flat_type': 'Flat Type',
                         'block': 'Block',
                         'street_name': 'Street',
                         'storey_range': 'Storey',
                         'floor_area_sqm': 'Floor Area (sqm)',
                         'flat_model': 'Model',
                         'lease_commence_date': 'Lease Start',
                         'remaining_lease': 'Remaining Lease',
                         'resale_price': 'Price (S$)'}
            )
            formatted_df = formatted_df.loc[:, formatted_df.columns != '_id']
            
            print("\nFiltered dataset: ")
            print(formatted_df.to_string(index=False, max_rows=15))
        elif choice == "2":
            show_summary_snapshot(df)
        elif choice == "3":
            show_town_ranking(df)
        elif choice == "4":
            plot_price_comparison_chart(df)
        elif choice == "5":
            print("👋 Exiting program. Thank you for exploring HDB data!")
            break
        else:
            print("❌ Invalid choice. Please try again.")

def apply_filters(df):
    # Arrange filters for user to pick from
    towns = sorted(df['town'].unique())
    flat_types = sorted(df['flat_type'].unique())
    months = sorted(df['month'].unique(), reverse=True)

    # Prompt user for filters
    print("\n=== Enter your filters (press Enter to skip) ===")
    print("\nAvailable Towns: ", ', '.join(towns))
    town = input("Enter Town: ").strip().upper()

    print("\nAvailable Flat Types: ", ', '.join(flat_types))
    flat_type = input("Enter Flat Type: ").strip().upper()

    print("\nAvailable Months: ", ', '.join(months))
    month = input("Enter Month (YYYY-MM): ").strip()

    filtered = df.copy()
    if town:
        filtered = filtered[filtered['town'] == town]
    if flat_type:
        filtered = filtered[filtered['flat_type'] == flat_type]
    if month:
        filtered = filtered[filtered['month'] == month]
    
    print(f"\nFilters entered: Town - {town}, Flat Type - {flat_type}, Month - {month}.")

    return filtered

def filter_dataframe(df, filters):
    # Apply filters to DataFrame dynamically.
    if filters["town"]:
        df = df[df["town"].str.upper() == filters["town"]]
    if filters["flat_type"]:
        df = df[df["flat_type"].str.upper() == filters["flat_type"]]
    if filters["month"]:
        df = df[df["month"] == filters["month"]]
    return df

if __name__ == "__main__":
    main()
