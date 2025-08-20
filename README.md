# EIA Crude Oil Data Pipeline

# Project Description
This project is a simple, end-to-end data pipeline built in Python. It extracts U.S. crude oil production data from the EIA's Open Data API, transforms the raw data, and loads it into a clean, local CSV file. This project demonstrates foundational data engineering skills using a command-line interface.

# Features
- Data Extraction: Connects to the EIA's v2 API to fetch crude oil production data.
- Data Transformation: Cleans raw data using the pandas library (renaming columns, handling data types).
- Data Loading: Persists the cleaned data to a local `eia_crude_oil_production.csv` file.
- Robustness: Includes unit tests with `pytest` and uses Python's  `logging` module for better error handling.

# How to Run the Script
1. Clone the Repository:
```bash
git clone [Repository URL here]
cd data-source-scraper
```

2. Install Dependencies:
```bash
pip install -r requirements.txt
```

3. Run the Script:
You will need a free API key from the EIA. Once you have it, run the script with your API key and the correct data route.
```bash
python main.py --api_key YOUR_API_KEY --route petroleum/crd/crpdn/data
```

# Technologies Used
- Python 3
- `requests` for API calls
- `pandas` for data manipulation
- `pytest` for unit testing
- `logging` for error handling






