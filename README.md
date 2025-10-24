# 🏠 HDB Resale Data Analysis (Singapore)
A Python project that fetches, filters, and visualizes Singapore HDB resale transaction data directly from [data.gov.sg](https://data.gov.sg/) public API.

This project showcases API integration, data analysis, and interactive CLI features — all within a clean, menu-driven interface.

## ⚙️ Features
- **Dynamic Data Fetching**

     Pulls resale data for a custom number of past months via the public API.

- **Interactive CLI Menu**

    Navigate easily through options to explore and visualize data.

- **Filtering Options**

    Filter transactions by **town**, **flat type**, or **month**.

- **Summary Snapshot**

    Displays:
    - Average resale price grouped by town
    - Highest-priced transaction overall

- **Town Ranking**

    Lists the **Top 5 Towns** by transaction volume.

- **Chart Comparison**

    Generates bar charts showing average price trends across all flat types.

## 📦 Installation
1. Install Python

    Ensure **Python 3.10+** is installed.
    
    You can check your version with `python --version`.

    If you don't have it, download it from [python.org/downloads](https://www.python.org/downloads/).

2. Clone this repository

    ```
    git clone https://github.com/bryancworks/hdb-resale-analytics.git
    
    cd hdb-resale-analytics
    ```

3. (Optional but recommended) Create a virtual environment

    ```
    python -m venv venv
    source venv/bin/activate    # macOS/Linux
    venv\Scripts\activate       # Windows
    ```

4. Install dependencies

    ```
    pip install -r requirements.txt
    ```

## 💻 Usage
Run the main script with an optional number of months to fetch:

_Range accepts 1-5 months. Default is 3 months if not specified._

```
python main.py --months 3
```
Once loaded, navigate the interactive menu:
```
1. Apply filters
2. View summary snapshot
3. View town ranking
4. Chart comparison
5. Exit
```

## 🔧 Tech Stack
- Python 3.10+
- Libraries: `pandas`, `requests`, `matplotlib`, `argparse`

## 📈 Example Output
Summary Snapshot

Town            | Price (S$)
--------------- | ---------------
CENTRAL AREA    | 950143
BISHAN          | 867430
BUKIT MERAH     | 752819
...             | ...