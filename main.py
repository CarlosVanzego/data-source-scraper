# Part 1: Importing Necessary Libraries
# These are the foundational tools for my data pipeline.
# 'argparse' is for handling command-line arguments.
# 'requests' is for making HTTP requests to APIs.
# 'pandas' is for data manipulation and analysis.
# 'json' is for working with JSON data, which is the format the API sends.
# 'os' is a built-in library that helps with operating system-level task, like creating directories.
import argparse
import requests
import pandas as pd
import json
import os 

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
# This is a reusable function that handles the complex logic of connecting to the API and dealing with potential errors.
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
    
# This function cleans and transforms the raw EIA data into a usable format.
def clean_eia_data(df):
    """
    Cleans and transforms the raw EIA DataFrame into a usable format.
    This function isolates the data quality and transformation logic.
    """
    print("Starting data cleaning...🧼")

    # Step 1: Rename columns for clarity.
    # The original API columns often have generic names ('period', 'value').
    # I renmame them to more descriptive, understandable names for analysis.
    df.rename(columns={'period': 'date', 'value': 'production_bbl_per_day'}, inplace=True)

    # Step 2: Convert the 'date' column to a proper datetime format.
    # Raw data is often a string; Converting it to a datetime object enables powerful time-series analysis with pandas.
    df['date'] = pd.to_datetime(df['date'], format='%Y-%m') # Format depends on my data

    # Step 3: Handle potential missing values (if any).
    # Dropping rows with any NaN values is a simple method for ensuring data quality.
    # This is a common first step in a data pipeline.
    df.dropna(inplace=True) 

    print("Data cleaning complete.")
    return df

# This function is responsible for writing the DataFrame to a file.
def save_data_to_csv(df, output_path):
    """
    Saves the DataFrame to a CSV file
    """
    # Create the output directory if it doesn't exist
    output_dir = os.path.dirname(output_path)
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)
        print(f"Created directory: {output_dir}")

    print(f"Saving data to {output_path}...")
    df.to_csv(output_path, index=False)
    print("Data successfully saved.")


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

        # Here I am calling my cleaning function
        cleaned_df = clean_eia_data(df)

        # These lines print the results to my terminal to verify the process.
        print("\nFirst 5 records retrieved and cleaned:")
        print(cleaned_df.head())
        print(f"\nFinal DataFrame shape: {cleaned_df.shape}")
    else:
        print("Failed to fetch data or 'data' key not found.") 