import requests
import json

# List to store combined results from all pages
all_results = []

for i in range(1, 6):
    url = "https://api.themoviedb.org/3/movie/popular?language=en-US&page=" + str(i)

    headers = {
        "accept": "application/json",
        "Authorization": "Bearer eyJhbGciOiJIUzI1NiJ9.eyJhdWQiOiI4MDg0MDRlY2QwNGQwMjQxMjhiMGJhMmY4OGJmNTk3YyIsIm5iZiI6MTcyNzk3MjAyMi4wNDI1OTMsInN1YiI6IjY2ZWMyZTI2NjJjNGJiMThjOTc0YTdkYiIsInNjb3BlcyI6WyJhcGlfcmVhZCJdLCJ2ZXJzaW9uIjoxfQ.aAC7sVBoQRODwDCg2ywn9henI6sfw7lJpTvV4sWMxg4"
    }

    response = requests.get(url, headers=headers)
    
    # Parse the JSON response
    data = response.json()
    
    # Extract the 'results' part and append to all_results
    results = data.get('results', [])
    all_results.extend(results)  # Combine results from all pages

# Write the combined results to a single file
with open("data/json_data/popular_movies.json", "w", encoding="utf-8") as file:
    json.dump(all_results, file, ensure_ascii=False, indent=4)
