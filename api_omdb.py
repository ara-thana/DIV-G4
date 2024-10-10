import requests
import json

# Your API key and base URL
api_key = '8501dc49'
base_url = 'http://www.omdbapi.com/'

# Query parameters
params = {
    'apikey': api_key,
    'page': 1  # This will increment for each page
}

# Container to hold all results
all_movies = []

# Loop through 100 pages
for page in range(1, 3):  # from page 1 to 100
    params['page'] = page
    response = requests.get(base_url, params=params)
    if response.status_code == 200:
        data = response.json()
        print(data)
        if 'Search' in data:
            all_movies.extend(data['Search'])
        else:
            print(f"No results found on page {page}")
    else:
        print(f"Error: Unable to retrieve data from page {page}")
        break  # Exit if there's an error

# Save to a JSON file
with open('omdb_movies.json', 'w') as json_file:
    json.dump(all_movies, json_file, indent=4)

print(f"Successfully saved {len(all_movies)} records to omdb_movies.json")
