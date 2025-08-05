import argparse 

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