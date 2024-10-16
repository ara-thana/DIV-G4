import requests
from bs4 import BeautifulSoup
import pandas as pd
import re
def obtener_url_wikipedia(titulo_pelicula, es_film=False):
    titulo_formateado = titulo_pelicula.replace(" ", "_")
    if es_film:
        titulo_formateado += '_(film)' 
    url_base = "https://en.wikipedia.org/wiki/"
    return url_base + titulo_formateado
def obtener_info_pelicula(titulo):
    url = obtener_url_wikipedia(titulo)
    response = requests.get(url)
    if response.status_code != 200:
        print(f"No se pudo acceder a la URL: {url}")
        return None
    soup = BeautifulSoup(response.text, 'html.parser')
    pelicula_info = {'Title': titulo}
    infobox = soup.find('table', {'class': 'infobox vevent'})
    if infobox:
        filas = infobox.find_all('tr')
        for fila in filas:
            clave = fila.find('th')
            valor = fila.find('td')
            if clave and valor:
                clave_texto = clave.text.strip()
                if 'Directed by' in clave_texto or 'Director' in clave_texto:
                    pelicula_info['Director'] = valor.text.strip()
                elif 'Starring' in clave_texto or 'Cast' in clave_texto:
                    actores = [a.text for a in valor.find_all('a')]
                    pelicula_info['Cast'] = ', '.join(actores)  
                    if actores:
                        pelicula_info['Lead'] = actores[0]  
                elif 'Release date' in clave_texto or 'Released' in clave_texto:
                    fecha_completa = valor.text.strip()
                    match = re.search(r'\b(19|20)\d{2}\b', fecha_completa)
                    if match:
                        pelicula_info['Release Year'] = match.group(0) 
                    else:
                        pelicula_info['Release Year'] = 'Unknown'  
                elif 'Produced by' in clave_texto or 'Production companies' in clave_texto:
                    pelicula_info['Production Companies'] = ', '.join([a.text for a in valor.find_all('a')])
                elif 'Running time' in clave_texto:
                    running_time_texto = valor.text.strip()
                    match_minutos = re.search(r'(\d+)\s*minutes', running_time_texto)
                    match_horas_minutos = re.search(r'(\d+)\s*hours?\s*(\d*)\s*minutes?', running_time_texto)
                    
                    if match_minutos:
                        pelicula_info['Running Time'] = match_minutos.group(1)  # Extraer solo el número de minutos
                    elif match_horas_minutos:
                        horas = int(match_horas_minutos.group(1))
                        minutos = int(match_horas_minutos.group(2)) if match_horas_minutos.group(2) else 0
                        total_minutos = horas * 60 + minutos
                        pelicula_info['Running Time'] = str(total_minutos)  
                    else:
                        pelicula_info['Running Time'] = 'Unknown'
                
                elif 'Country' in clave_texto:
                    pelicula_info['Country'] = valor.text.strip()
                elif 'Language' in clave_texto:
                    pelicula_info['Language'] = valor.text.strip()
                elif 'IMDb' in clave_texto:
                    pelicula_info['IMDB Rating'] = valor.text.strip()
                elif 'Metacritic' in clave_texto or 'Metascore' in clave_texto:
                    pelicula_info['Metascore'] = valor.text.strip()
                elif 'Rating' in clave_texto or 'MPAA' in clave_texto or 'Censorship' in clave_texto:
                    pelicula_info['Censorship Rating'] = valor.text.strip()
    if not infobox:
        print(f"No se encontró información relevante en '{titulo}'. Probando con '_(film)'...")
        return obtener_info_pelicula_film(titulo)
    return pelicula_info
def obtener_info_pelicula_film(titulo):
    url = obtener_url_wikipedia(titulo, es_film=True)
    response = requests.get(url)
    if response.status_code != 200:
        print(f"No se pudo acceder a la URL: {url}")
        return None
    soup = BeautifulSoup(response.text, 'html.parser')
    pelicula_info = {'Title': titulo }
    infobox = soup.find('table', {'class': 'infobox vevent'})
    if infobox:
        filas = infobox.find_all('tr')
        for fila in filas:
            clave = fila.find('th')
            valor = fila.find('td')
            if clave and valor:
                clave_texto = clave.text.strip()
                
                if 'Directed by' in clave_texto or 'Director' in clave_texto:
                    pelicula_info['Director'] = valor.text.strip()
                
                elif 'Starring' in clave_texto or 'Cast' in clave_texto:
                    pelicula_info['Lead'] = ', '.join([a.text for a in valor.find_all('a')])
                
                elif 'Release date' in clave_texto or 'Released' in clave_texto:
                    pelicula_info['Year'] = valor.text.strip()
                
                elif 'Produced by' in clave_texto or 'Production companies' in clave_texto:
                    pelicula_info['Production Companies'] = ', '.join([a.text for a in valor.find_all('a')])
                
                elif 'Running time' in clave_texto:
                    pelicula_info['Running Time'] = valor.text.strip()
                
                elif 'Country' in clave_texto:
                    pelicula_info['Country'] = valor.text.strip()

                elif 'Language' in clave_texto:
                    pelicula_info['Language'] = valor.text.strip()
                
                elif 'IMDb' in clave_texto:
                    pelicula_info['IMDB Rating'] = valor.text.strip()
                
                elif 'Metacritic' in clave_texto or 'Metascore' in clave_texto:
                    pelicula_info['Metascore'] = valor.text.strip()
                elif 'Rating' in clave_texto or 'MPAA' in clave_texto or 'Censorship' in clave_texto:
                    pelicula_info['Censorship Rating'] = valor.text.strip()

    if 'Director' not in pelicula_info or 'Lead Actor/Actress' not in pelicula_info or 'Year' not in pelicula_info:
        return None 
    return pelicula_info

def leer_titulos_desde_excel(ruta_archivo):
    df = pd.read_excel(ruta_archivo)
    print(f"Columnas del archivo: {df.columns.tolist()}")  
    return df['Title'].dropna().tolist()

def guardar_en_excel(datos_peliculas, nombre_archivo):
    df = pd.DataFrame(datos_peliculas)
    df.to_excel(nombre_archivo, index=False)

ruta_archivo_excel = '../data/output/movies_and_platforms.xlsx'
titulos_peliculas = leer_titulos_desde_excel(ruta_archivo_excel)
peliculas_info = []
for titulo in titulos_peliculas:
    info_pelicula = obtener_info_pelicula(titulo)
    if info_pelicula:
        peliculas_info.append(info_pelicula)
nombre_archivo_salida = '../data/output/informacion_peliculas_scraping.xlsx'
guardar_en_excel(peliculas_info, nombre_archivo_salida)
print(f"Información de las películas guardada en '{nombre_archivo_salida}'")
