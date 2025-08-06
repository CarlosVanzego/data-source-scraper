# import argparse 
# import requests
# from config import API_KEY
# import pandas as pd

# # 1. Create a parser object
# # The 'description' argument provides a quick summary when the user asks for help.
# parser = argparse.ArgumentParser(description="This script fetches U.S. Crude Oil production data from the EIA API.")

# # 2. Add arguments to the parser for my API key and route
# # 'help' provides a description of the arguments.
# parser.add_argument("--api_key", type=str, required=True, help="My personal EIA API key.")
# parser.add_argument("--route", type=str, required=True, help="The EIA API route for the data")

# # 3. Parse the arguments
# # This line runs the parser and stores the values in a variable called 'args'.
# args = parser.parse_args()

# # 4. Use the arguments
# print(f"Fetching data from route: '{args.route}' using API Key: '{args.api_key}'")

 
# def fetch_eia_data(api_key, route):
#     # The base URL for the eia search endpoint
#     base_url = "https://api.eia.gov"
#     full_url = f"{base_url}/{route}?api_key={api_key}"

#     try:
#         response = requests.get(full_url, timeout=10)
#         response.raise_for_status() # This will handle HTTP errors
#         return response.json()
#     except requests.exceptions.RequestException as e:
#         print(f"An error occured: {e}")
#         return None
    
# if __name__ == "__main__":
#     print(f"Fetching data from route: {args.route}")
#     # The route should not have a leading slash
#     route_without_slash = args.route.strip('/')
#     eia_data = fetch_eia_data(args.api_key, route_without_slash)

#     if eia_data and "data" in eia_data.get("response", {}):
#         data_records = eia_data["response"]["data"]
#         df = pd.DataFrame(data_records)
#         print(f"DataFrame created with {df.shape[0]} rows and {df.shape[1]} columns.")
#         print("First 5 records retrieved:")
#         print(df.head())
#     else:
#         print("Failed to fetch data or 'data' key not found.")