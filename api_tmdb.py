import requests
import pandas as pd

# the api key the send me
API_KEY = 'cba190ef9c3740680be42e38521db35e'

base_url = 'https://api.themoviedb.org/3/'
def obtener_plataformas(movie_id):
    watch_providers_url = f'{base_url}movie/{movie_id}/watch/providers'
    provider_params = {
        'api_key': API_KEY
    }
    
    response = requests.get(watch_providers_url, params=provider_params)
    
    if response.status_code != 200:
        return []
    
    providers_data = response.json()
    if 'results' in providers_data and 'US' in providers_data['results']:
        plataformas = providers_data['results']['US'].get('flatrate', [])
        return [plataforma['provider_name'] for plataforma in plataformas]
    return []
def obtener_peliculas_populares(max_paginas=5):
    popular_url = f'{base_url}movie/popular'
    peliculas = []
    
    for pagina in range(1, max_paginas + 1):
        params = {
            'api_key': API_KEY,
            'language': 'en',
            'page': pagina
        }
        
        response = requests.get(popular_url, params=params)
        
        if response.status_code != 200:
            print(f"Error al obtener la página {pagina}: {response.status_code}")
            break
        
        data = response.json()
        resultados = data.get('results', [])
        
        if not resultados:
            break
        
        peliculas.extend(resultados)
    
    return peliculas

def crear_excel_peliculas(peliculas):
    lista_datos = []
    titulos_vistos = set()  
    
    for pelicula in peliculas:
        titulo = pelicula['title']
        if titulo in titulos_vistos:
            continue
        titulos_vistos.add(titulo)
        
        movie_id = pelicula['id']
        plataformas = obtener_plataformas(movie_id)
        
        if not plataformas:
            plataformas = ["Not available"]# means no platform was found
        lista_datos.append({
            'Title': titulo,
            'Platforms': ', '.join(plataformas)
        })
    df = pd.DataFrame(lista_datos)
    df.to_excel('movies_and_platforms.xlsx', index=False)
    print("Excel file created successfully: movies_and_platforms.xlsx")

todas_las_peliculas_populares = obtener_peliculas_populares(max_paginas=10)  # We look up to 10 pages
crear_excel_peliculas(todas_las_peliculas_populares)