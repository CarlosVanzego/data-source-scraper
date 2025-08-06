import argparse
import requests
import pandas as pd
import json

# My argparse code for command-line arguments
parser = argparse.ArgumentParser(description="Fetches U.S. Crude Oil production data from the EIA API.")
parser.add_argument("--api_key", type=str, required=True, help="My personal EIA API Key.")
parser.add_argument("--route", type=str, required=True, help="The EIA API route for the data.")
args = parser.parse_args()

def fetch_eia_data(api_key, route):
    """
    Fetches data from the EIA API using the provided API key and route
    """
    # The base URL for the EIA API.
    base_url = "https://api.eia.gov"

    # Strip any leading/trailing slashes form the route for clean URL construction
    clean_route = route.strip('/')

    # The full URL for the GET request
    full_url = f"{base_url}/v2/{clean_route}?api_key={api_key}"

    print(f"Attempting to fetch data from: {full_url}") # This line is for debugging

    try:
        response = requests.get(full_url, timeout=10, verify=False) # Added 'verify=False' to tell Python to skip the security check and trust the connection as this was raising an error when running my code.
        # This will raise an exception for HTTP error codes (4xx or 5xx)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        print(f"An error occured: {e}")
        return None

if __name__ == "__main__":
    print(f"Fetching data from route: {args.route}")

    eia_data = fetch_eia_data(args.api_key, args.route)

    if eia_data and "data" in eia_data.get("response", {}):
        data_records = eia_data["response"]["data"]
        df = pd.DataFrame(data_records)
        print(f"\nDataFrame created with {df.shape[0]} rows and {df.shape[1]} columns.")
        print("First 5 records retrieved")
        print(df.head())
    else:
        print("Failed to fetch data or 'data' key not found.") 