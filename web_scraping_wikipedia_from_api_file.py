import requests
from bs4 import BeautifulSoup
import pandas as pd

def obtener_url_wikipedia(titulo_pelicula, es_film=False):
    titulo_formateado = titulo_pelicula.replace(" ", "_")
    if es_film:
        titulo_formateado += '_(film)'  # Add "_(film)" if necessary, since there are some pages with the same name in wikipedia
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
    # (infobox)
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
                    pelicula_info['Cast'] = ', '.join([a.text for a in valor.find_all('a')])
                elif 'Release date' in clave_texto or 'Released' in clave_texto:
                    pelicula_info['Release Year'] = valor.text.strip()
                elif 'Produced by' in clave_texto or 'Production companies' in clave_texto:
                    pelicula_info['Production Companies'] = ', '.join([a.text for a in valor.find_all('a')])
                    pelicula_info['Running Time'] = valor.text.strip()
                elif 'Rating' in clave_texto or 'Rated' in clave_texto:
                    pelicula_info['Rating'] = valor.text.strip()

    #  "_(film)" case
    if not infobox:
        print(f"Not relevant info on  '{titulo}'.Trying with '_(film)'...")
        return obtener_info_pelicula_film(titulo)
    return pelicula_info

# FTry again with "_(film)"
def obtener_info_pelicula_film(titulo):
    url = obtener_url_wikipedia(titulo, es_film=True)
    response = requests.get(url)
    if response.status_code != 200:
        print(f"No se pudo acceder a la URL: {url}")
        return None
    soup = BeautifulSoup(response.text, 'html.parser')
    pelicula_info = {'Title': titulo } #+ ' (film)'
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
                    pelicula_info['Cast'] = ', '.join([a.text for a in valor.find_all('a')])
                elif 'Release date' in clave_texto or 'Released' in clave_texto:
                    pelicula_info['Release Year'] = valor.text.strip()
                elif 'Produced by' in clave_texto or 'Production companies' in clave_texto:
                    pelicula_info['Production Companies'] = ', '.join([a.text for a in valor.find_all('a')])
                elif 'Running time' in clave_texto:
                    pelicula_info['Running Time'] = valor.text.strip()
                elif 'Rating' in clave_texto or 'Rated' in clave_texto:
                    pelicula_info['Rating'] = valor.text.strip()
    if 'Director' not in pelicula_info or 'Cast' not in pelicula_info or 'Release Year' not in pelicula_info:
        return None 
    return pelicula_info
def leer_titulos_desde_excel(ruta_archivo):
    df = pd.read_excel(ruta_archivo)
    print(f"Columnas del archivo: {df.columns.tolist()}")  # Verificar columnas
    return df['Title'].dropna().tolist()
def guardar_en_excel(datos_peliculas, nombre_archivo):
    df = pd.DataFrame(datos_peliculas)
    df.to_excel(nombre_archivo, index=False)
ruta_archivo_excel = r'C:\Users\María Fernández\Documents\4º año\DIV\movies_and_platforms.xlsx'
titulos_peliculas = leer_titulos_desde_excel(ruta_archivo_excel)
peliculas_info = []
for titulo in titulos_peliculas:
    info_pelicula = obtener_info_pelicula(titulo)
    if info_pelicula:
        peliculas_info.append(info_pelicula)
nombre_archivo_salida = 'informacion_peliculas_scraping.xlsx'
guardar_en_excel(peliculas_info, nombre_archivo_salida)

print(f"Información de las películas guardada en '{nombre_archivo_salida}'")
