import requests
import pandas as pd

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

def obtener_detalles_pelicula(movie_id):
    movie_details_url = f'{base_url}movie/{movie_id}'
    details_params = {
        'api_key': API_KEY,
        'language': 'en'
    }
    response = requests.get(movie_details_url, params=details_params)
    if response.status_code != 200:
        return None
    return response.json()
def obtener_clasificacion_edad(movie_id):
    url_clasificacion = f'{base_url}movie/{movie_id}/release_dates'
    params = {
        'api_key': API_KEY
    }
    response = requests.get(url_clasificacion, params=params)
    if response.status_code != 200:
        return 'Not available'
    clasificaciones_data = response.json()
    clasificaciones = clasificaciones_data.get('results', [])
    for clasificacion in clasificaciones:
        if clasificacion['iso_3166_1'] == 'US': 
            for release in clasificacion['release_dates']:
                return release.get('certification', 'Not available')
    return 'Not available'
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
        print("Obteniendo detalles de la película:", titulo)
        movie_id = pelicula['id']
        detalles = obtener_detalles_pelicula(movie_id)
        if detalles is None:
            continue
        plataformas = obtener_plataformas(movie_id)
        if not plataformas:
            plataformas = ["Not available"]
        recaudacion = detalles.get('revenue', 'N/A')
        sinopsis = detalles.get('overview', 'N/A')
        calificacion_publico = detalles.get('vote_average', 'N/A')
        conteo_votos_publico = detalles.get('vote_count', 'N/A')
        popularidad = detalles.get('popularity', 'N/A')
        generos = ', '.join([genero['name'] for genero in detalles.get('genres', [])])
        clasificacion_edad = obtener_clasificacion_edad(movie_id)
        lista_datos.append({
            'Title': titulo,
            'Platforms': ', '.join(plataformas),
            'Revenue': recaudacion,
            'Synopsis': sinopsis,
            'Audience Rating': calificacion_publico,
            'Vote Count': conteo_votos_publico,
            'Popularity': popularidad,
            'Genres': generos,
            'Censorship Rating': clasificacion_edad          })
    
    df = pd.DataFrame(lista_datos)
    df.to_excel('../data/output/movies_and_platforms.xlsx', index=False)
todas_las_peliculas_populares = obtener_peliculas_populares(max_paginas=40)
crear_excel_peliculas(todas_las_peliculas_populares)
