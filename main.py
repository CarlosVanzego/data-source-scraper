# Part 1: Importing Necessary Libraries
# These are the foundational tools for my data pipeline.
# 'argparse' is for handling command-line arguments.
# 'requests' is for making HTTP requests to APIs.
# 'pandas' is for data manipulation and analysis.
# 'json' is for working with JSON data, which is the format the API sends.
import argparse
import requests
import pandas as pd
import json

# Part 2: Set up Command-Line Arguments
# This section makes my script flexible. Instead of harcoding values.
# I can pass them in when I run the script from the terminal.
parser = argparse.ArgumentParser(description="Fetches U.S. Crude Oil production data from the EIA API.")
# Here I am requiring two pieces of information: the API key and the data route.
parser.add_argument("--api_key", type=str, required=True, help="My personal EIA API Key.")
parser.add_argument("--route", type=str, required=True, help="The EIA API route for the data.")
# I'm then storing the parsed arguments into a variable called 'args'
args = parser.parse_args()

# Part 3: Define the Core Functionality (API Call)
# This is a reusable function that handles the cmoplex logic of connecting to the API and dealing with potential errors.
def fetch_eia_data(api_key, route):
    """
    Fetches data from the EIA API using the provided API key and route
    """
    # The base URL is th emain entry point for the EIA's API.
    base_url = "https://api.eia.gov"

    # I used the Strip function to strip any leading/trailing slashes form the route for clean/correct URL construction.
    clean_route = route.strip('/')

    # I built the complete URL by combining the base, the API version, the route, and teh API key; for the GET request.
    full_url = f"{base_url}/v2/{clean_route}?api_key={api_key}"

    print(f"Attempting to fetch data from: {full_url}") # This line is for debugging

    try:
        # Here I make the actual GET request to the URL.
        # 'timeout=10' prevents the script from hanging forever if there's no response.
        response = requests.get(full_url, timeout=10, verify=False) 
        # 'verify=False' temporarily disables the SSL certificate check and tells Python to trust the connection as this was raising an error when running my code in development.

        # This line checks the HTTP status code.
        # If the code is 4xx or 5xx, it raises an exception to stop the program.
        response.raise_for_status()

        # I return the data as a Python Dictionary.
        return response.json()
    
    except requests.exceptions.RequestException as e:
        # This block catches any errors during the request (e.g., connection issues, 500 errors)
        print(f"An error occured: {e}")
        return None
    

# Part 4: Execute the Script (The main entry point)
# The 'if __name__ == "__main__":' block ensures this code only runs when the script is executed directly (not when imported as a module)
if __name__ == "__main__":
    print(f"Fetching data from route: {args.route}")

    # Here I call my function to get the raw data from the API.
    eia_data = fetch_eia_data(args.api_key, args.route)

    # This line checks if the data was successfully fetched and contains the 'data' key.
    # This is a defensive check to prevent errors down the line.
    if eia_data and "data" in eia_data.get("response", {}):
        # This line extracts the list of records from the nested JSON structure.
        data_records = eia_data["response"]["data"]

        # This line creates a Pandas DataFrame, which is the table-like structure I want.
        df = pd.DataFrame(data_records)
        print(f"\nDataFrame created with {df.shape[0]} rows and {df.shape[1]} columns.")
        print("First 5 records retrieved")
        print(df.head())
    else:
        print("Failed to fetch data or 'data' key not found.") 

def clean_eia_data(df):
    """
    Cleans and transforms EIA data DataFrame
    """
    print("Starting data cleaning...🧼")
    # Step 1: Rename columns for clarity
    df.rename(columns={'period': 'date', 'value': 'production_bbl_per_day'}, inplace=True)

    # Step 2: Convert the data column into datetime objects
    df['date'] = pd.to_datetime(df['date'], format='%Y-%m') # Format depends on my data

    # Step 3: Handle potential missing values (if any)
    df.dropna(inplace=True) 

    # More cleaning or filtering steps here
    print("Data cleaning complete.")
    return df

if __name__ == "__main__":
    print(f"Fetching data from route: {args.route}")
    eia_data = fetch_eia_data(args.api_key, args.route)

    if eia_data and "data" in eia_data.get("response", {}):
        data_records = eia_data["response"]["data"]
        df = pd.DataFrame(data_records)

        # Here I am calling my new cleaning function
        cleaned_df = clean_eia_data(df)

        print("First 5 cleaned records:")
        print(cleaned_df.head())
        print(f"Failed to fetch data or 'data' key not found.")