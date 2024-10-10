import requests
import pandas as pd
from datetime import datetime
from bs4 import BeautifulSoup

# Define tu User-Agent personalizado
user_agent = 'Sandra917/1.0 (contacto: sandramorandin179@gmail.com)'

# Agrega tu API Key de OMDb aquí
omdb_api_key = 'e4dbcc92'

# Función para buscar películas en un año específico (de Wikipedia)
def buscar_peliculas_por_año(año):
    url = f"https://en.wikipedia.org/w/api.php"
    params = {
        'action': 'query',
        'list': 'search',
        'srsearch': f"films {año}",
        'format': 'json',
        'utf8': 1,
        'srlimit': 50  # Limitamos a 50 resultados por búsqueda
    }

    response = requests.get(url, params=params, headers={'User-Agent': user_agent})
    data = response.json()
    
    peliculas = []
    if 'query' in data:
        for item in data['query']['search']:
            peliculas.append(item['title'])
    
    return peliculas

# Función para obtener información de una película desde Wikipedia
def obtener_informacion_pelicula(titulo):
    # Reemplaza los espacios por guiones bajos para la URL
    url_titulo = titulo.replace(' ', '_')
    url = f"https://en.wikipedia.org/wiki/{url_titulo}"
    
    # Realiza la solicitud a la página de la película
    response = requests.get(url, headers={'User-Agent': user_agent})

    if response.status_code == 200:
        soup = BeautifulSoup(response.text, 'html.parser')

        # Inicializa el diccionario para almacenar los datos de la película
        datos_pelicula = {
            'titulo': titulo,
            'anio': None,
            'genero': None,   # Se obtendrá más adelante de OMDb
            'director': None,
            'casting': None,
            'rating': None    # Se obtendrá más adelante de OMDb
        }

        # Buscando el infobox de la película
        infobox = soup.find('table', class_='infobox')
        if infobox:
            for row in infobox.find_all('tr'):
                header = row.find('th')
                if header:
                    header_text = header.text.strip().lower()  # Usamos lower para evitar problemas de mayúsculas/minúsculas
                    if 'release date' in header_text or 'year' in header_text:
                        datos_pelicula['anio'] = row.find('td').text.strip().split('(')[0]  # Extraemos solo la fecha
                    elif 'director' in header_text or 'directed by' in header_text:
                        datos_pelicula['director'] = row.find('td').text.strip()
                    elif 'starring' in header_text or 'cast' in header_text:
                        datos_pelicula['casting'] = row.find('td').text.strip()

        return datos_pelicula
    else:
        print(f"Error al obtener información de {titulo}: {response.status_code}")
        return None

# Función para obtener información adicional (género y rating) de OMDb
def obtener_datos_omdb(titulo):
    url = f"http://www.omdbapi.com/?t={titulo}&apikey={omdb_api_key}"
    
    response = requests.get(url)
    
    # Imprimir el código de estado y el contenido de la respuesta
    print(f"Solicitud a OMDb: {url}")
    print(f"Código de estado: {response.status_code}")
    print(f"Contenido de la respuesta: {response.text}")

    if response.status_code == 200 and response.text:
        data = response.json()
        if data.get('Response') == 'True':
            datos_omdb = {
                'genero': data.get('Genre', None),    # Obtiene el género de la película
                'rating': data.get('imdbRating', None)  # Obtiene el rating de IMDb
            }
            return datos_omdb
    else:
        print(f"No se encontró información de OMDb para {titulo} o la solicitud falló")
    return None


# Rango de años
ano_actual = datetime.now().year
rango_años = range(ano_actual - 10, ano_actual + 1)

# Lista para almacenar la información de las películas
peliculas_info = []

# Extraer la información de las películas
for año in rango_años:
    peliculas = buscar_peliculas_por_año(año)

    for pelicula in peliculas:
        info_wikipedia = obtener_informacion_pelicula(pelicula)
        
        if info_wikipedia:
            # Obtener datos de OMDb
            info_omdb = obtener_datos_omdb(pelicula)
            
            if info_omdb:
                # Mezclar la información de OMDb con la de Wikipedia
                info_wikipedia['genero'] = info_omdb.get('genero')
                info_wikipedia['rating'] = info_omdb.get('rating')
            
            print(f"Información combinada: {info_wikipedia}")
            peliculas_info.append(info_wikipedia)

# Crear un DataFrame de pandas
df = pd.DataFrame(peliculas_info)

# Guardar en un archivo Excel
df.to_excel('peliculas_info_ultimos_10_anios.xlsx', index=False)

print("Información de películas extraída y guardada en peliculas_info_ultimos_10_anios.xlsx")
