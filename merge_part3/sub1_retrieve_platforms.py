import pandas as pd
import requests
from concurrent.futures import ThreadPoolExecutor, as_completed
import time
API_KEY = 'cba190ef9c3740680be42e38521db35e'  
file_path = '../data/output/merged2.xlsx' 
df = pd.read_excel(file_path, sheet_name='Sheet1')
def get_tmdb_data(title):
    try:
        search_url = f"https://api.themoviedb.org/3/search/multi?api_key={API_KEY}&query={title}"
        response = requests.get(search_url)
        data = response.json()
        if data['results']:
            item = data['results'][0]
            production_companies = ', '.join([company['name'] for company in item.get('production_companies', [])])
            if item['media_type'] in ['movie', 'tv']:
                platforms_url = f"https://api.themoviedb.org/3/{item['media_type']}/{item['id']}?api_key={API_KEY}&append_to_response=watch/providers"
                platforms_response = requests.get(platforms_url)
                platforms_data = platforms_response.json()
                if 'results' in platforms_data.get('watch/providers', {}):
                    available_on = ', '.join([provider['provider_name'] for provider in platforms_data['watch/providers']['results'].get('US', {}).get('flatrate', [])])
                    return production_companies, available_on
            return production_companies, 'Not available'
    except Exception as e:
        print(f"Error al obtener datos de TMDB para '{title}': {e}")
    return 'Not available', 'Not available'


production_companies_list = []
platforms_list = []
max_workers = 10 
with ThreadPoolExecutor(max_workers=max_workers) as executor:
    futures = {executor.submit(get_tmdb_data, title): title for title in df['Title']}
    for future in as_completed(futures):
        title = futures[future]
        production_companies, platforms = future.result()
        production_companies_list.append(production_companies)
        platforms_list.append(platforms)
        print(f"Datos obtenidos para: {title} - Compañía: {production_companies} - Plataformas: {platforms}")
        time.sleep(0.1)
df['Production Companies'] = production_companies_list
df['Platforms'] = platforms_list
df.to_excel('../data/output/archivo_actualizado_tmdb.xlsx', index=False)
print("Archivo guardado con éxito.")
