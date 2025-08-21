import argparse
import requests
import pandas as pd
import json
import os 
import logging

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

parser = argparse.ArgumentParser(description="Fetches U.S. Crude Oil production data from the EIA API.")
parser.add_argument("--api_key", type=str, required=True, help="My personal EIA API Key.")
parser.add_argument("--route", type=str, required=True, help="The EIA API route for the data.")
args = parser.parse_args()


def fetch_eia_data(api_key, route):
    """
    Fetches data from the EIA API using the provided API key and route
    """
    base_url = "https://api.eia.gov"

    clean_route = route.strip('/')

    full_url = f"{base_url}/v2/{clean_route}?api_key={api_key}"

    logging.info(f"Attempting to fetch data from: {full_url}")

    try:
        response = requests.get(full_url, timeout=10, verify=False) 

        response.raise_for_status()

        logging.info("Data fetched successfully.")

        return response.json()
    
    except requests.exceptions.RequestException as e:
        logging.error(f"An error occured: {e}")
        return None
    
def clean_eia_data(df):
    """
    Cleans and transforms the raw EIA DataFrame.

    Args:
        df: The raw DataFrame from the EIA API

    Returns:
        A cleaned and trasnfomed DataFrame.
    """
    logging.info("Starting data cleaning...🧼")

    
    df.rename(columns={'period': 'date', 'value': 'production_bbl_per_day'}, inplace=True)

    df['date'] = pd.to_datetime(df['date'], format='%Y-%m')

    df.dropna(inplace=True) 

    logging.info("Data cleaning complete.")
    return df

def save_data_to_csv(df, output_path):
    """
    Saves the DataFrame to a CSV file.

    Args:
        df: The DataFrame to save.
        output_data: The file path to save the data to.
    """
    output_dir = os.path.dirname(output_path)
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)
        logging.info(f"Created directory: {output_dir}")
    logging.info(f"Saving data to {output_path}...")
    df.to_csv(output_path, index=False)
    logging.info("Data successfully saved.")


if __name__ == "__main__":

    eia_data = fetch_eia_data(args.api_key, args.route)

    if eia_data and "data" in eia_data.get("response", {}):
        data_records = eia_data["response"]["data"]

        df = pd.DataFrame(data_records)

        cleaned_df = clean_eia_data(df)
        output_file = 'output/eia_crude_oil_production.csv'
        save_data_to_csv(cleaned_df, output_file)
        logging.info("Pipeline executed succesfully.")

    else:
        logging.info("Pipeline failed to execute.")
