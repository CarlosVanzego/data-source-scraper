import argparse 
import requests
from config import API_KEY
import pandas as pd

# 1. Create a parser object
# The 'description' argument provides a quick summary when the user asks for help.
parser = argparse.ArgumentParser(description="This script will fetch and process data from a public API.")

# 2. Add arguments to the parser
# I'm adding one simple argument: a 'query'. This is what the user will type after the script name.
# 'help' provides a description of the argument.
parser.add_argument("query", type=str, help="The search term to be sent to the API.")

# 3. Parse the arguments
# This line runs the parser and stores the values in a variable called 'args'.
args = parser.parse_args()

# 4. Use the arguments
# I can now access the values of the 'query' argument using 'args.query'.
print(f"You requested data for the search term: '{args.query}'")

def search_movies(query):
    # The base URL for the movie search endpoint
    search_url = "https://api.themoviedb.org/3/search/movie"

    # The parameters to send with the request
    params = {
        "api_key": API_KEY,
        "query": query # Use the query from argparse
    }

    # Make the GET request to the API
    response = requests.get(search_url, params=params)

    # Error handling and data processing 
    return response 

if __name__ == "__main__":
    # Assuming args.query is the search term from argparse
    response = search_movies(args.query)

    # Check for a successful response 
    if response.status_code == 200:
        data = response.json()
        # The actual movie data is in the 'results' key
        movie_list = data.get("results", [])

        if movies_list:
            df = pd.DataFrame(movie_list)
            print(f"DataFrame created with {df.shape[0]} rows and {df.shape[1]} colunms.")
            print("First 5 movies retrieved:")
            # Let's print the 'title' and 'release_date' to see what we got
            print(df[['title', 'release_date', 'vote_average']].head())
        else:
            print("No movies found for that query.")
    else: 
        print(f"Error fetching data. Status code: {response.status_code}")