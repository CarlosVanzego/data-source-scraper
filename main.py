# Part 1: Importing Necessary Libraries
# These are the foundational tools for my data pipeline.
# 'argparse' is for handling command-line arguments.
# 'requests' is for making HTTP requests to APIs.
# 'pandas' is for data manipulation and analysis.
# 'json' is for working with JSON data, which is the format the API sends.
# 'os' is a built-in library that helps with operating system-level task, like creating directories.
# 'logging' is a module that emits log messages from programs; It's used to record events that occur during the execution of an application.
import argparse
import requests
import pandas as pd
import json
import os 
import logging


# Configuring the logging module 
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')


# Part 2: Set up Command-Line Arguments
# This section makes my script flexible. Instead of harcoding values.
# I can pass them in when I run the script from the terminal.
parser = argparse.ArgumentParser(description="Fetches U.S. Crude Oil production data from the EIA API.")
# Here I am requiring two pieces of information: the API key and the data route.
parser.add_argument("--api_key", type=str, required=True, help="My personal EIA API Key.")
parser.add_argument("--route", type=str, required=True, help="The EIA API route for the data.")
# I'm then storing the parsed arguments into a variable called 'args'
args = parser.parse_args()


# Part 3: Define the Core Functions (API call)
# This is a reusable function that handles the logic of connecting to the API and dealing with potential errors; It takes the parameters 'api_key' and 'route', this is where my command in the command-line will take those two pieces of information, then the function returns that data from the EIA API.
def fetch_eia_data(api_key, route):
    """
    Fetches data from the EIA API using the provided API key and route.

     Args:
        api_key: the given API key.

        route: the route to the specific data (i.e. petroleum/crd/crpdn/data)

    Returns:
        A cleaned and transformed DataFrame.
    """
    # The base URL is the main entry point for the EIA's API.
    base_url = "https://api.eia.gov"

    # I used the Strip function to strip any leading/trailing slashes form the route for clean/correct URL construction.
    clean_route = route.strip('/')

    # I built the complete URL by combining the base, the API version, the route, and the API key; for the GET request.
    full_url = f"{base_url}/v2/{clean_route}?api_key={api_key}"

    # Using this line instead of a print statement stating the data is being fetched.
    logging.info(f"Attempting to fetch data from: {full_url}")

    try:
        # Here I make the actual GET request to the URL.
        # 'timeout=10' prevents the script from hanging forever if there's no response.
        # 'verify=False' temporarily disables the SSL certificate check and tells Python to trust the connection as this was raising an error when running my code in development.
        response = requests.get(full_url, timeout=10, verify=False) 

        # This line checks the HTTP status code.
        # If the code is 4xx or 5xx, it raises an exception to stop the program.
        response.raise_for_status()

        logging.info("Data fetched successfully.")

        # I return the data as a Python Dictionary.
        return response.json()
    
    except requests.exceptions.RequestException as e:
        # This block catches any errors during the request (e.g., connection issues, 500 errors)    
        logging.error(f"An error occured: {e}")
        return None
    
# This function cleans and transforms the raw EIA data from the API into a usable format; it takes the parameter 'df' (short for DataFrame) which is the data being cleaned and the function returns the newly cleaned data.
def clean_eia_data(df):
    """
    Cleans and transforms the raw EIA DataFrame.

    Args:
        df: The raw DataFrame from the EIA API

    Returns:
        A cleaned and transformed DataFrame.
    """
    logging.info("Starting data cleaning...🧼")

    # Step 1: Rename columns for clarity.
    # The original API columns often have generic names ('period', 'value').
    # I renmame them to more descriptive, understandable names for analysis.
    df.rename(columns={'period': 'date', 'value': 'production_bbl_per_day'}, inplace=True)

    # Step 2: Converting the 'date' column to a proper datetime format.
    # Raw data is often a string; Converting it to a datetime object enables powerful time-series analysis with pandas.
    df['date'] = pd.to_datetime(df['date'], format='%Y-%m') # Format depends on my data

    # Step 3: Handle potential missing values (if any).
    # I'm using the 'dropna' function for dropping rows with any NaN values; This is a method for ensuring data quality and a common first step in a data pipeline.
    df.dropna(inplace=True) 

    logging.info("Data cleaning complete.")
    return df

# This function is responsible for writing the DataFrame to a file; I use the params 'df' (the dataframe), and 'output_path' which is the final destination of the data (the csv file); This function does not return anything because its saving the data to the csv file.
def save_data_to_csv(df, output_path):
    """
    Saves the DataFrame to a CSV file.

    Args:
        df: The DataFrame to save.
        output_data: The file path to save the data to.
    """
    # Create the output directory if it doesn't exist
    output_dir = os.path.dirname(output_path)
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)
        logging.info(f"Created directory: {output_dir}")
    logging.info(f"Saving data to {output_path}...")
    # This line prints a statemement letting me know the data has been successfully saved to the csv file.
    df.to_csv(output_path, index=False)
    logging.info("Data successfully saved.")


# Part 4: Execute the Script (The main entry point)
# The 'if __name__ == "__main__":' block ensures this code only runs when the script is executed directly (not when imported as a module)
if __name__ == "__main__":

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
        output_file = 'output/eia_crude_oil_production.csv'
        save_data_to_csv(cleaned_df, output_file)
        logging.info("Pipeline executed succesfully.")

        # These lines print the results to my terminal to verify the process of information that.
    else:
        logging.info("Pipeline failed to execute.")
