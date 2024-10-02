import requests
import json

# URL del archivo raw en GitHub
url = 'https://raw.githubusercontent.com/prust/wikipedia-movie-data/master/movies.json'

# Hacer la solicitud HTTP al archivo
response = requests.get(url)

# Verificar que la solicitud fue exitosa
if response.status_code == 200:
    # Cargar el contenido como JSON
    movie_data = response.json()

    # Extraer y mostrar algunos datos de ejemplo
    for movie in movie_data[:5]:  # Muestra los primeros 5 películas
        title = movie.get('title', 'Sin título')
        year = movie.get('year', 'Año no disponible')
        cast = movie.get('cast', [])
        genres = movie.get('genres', [])
        
        print(f"Título: {title}")
        print(f"Año: {year}")
        print(f"Reparto: {', '.join(cast)}")
        print(f"Géneros: {', '.join(genres)}")
        print('-' * 40)

    # Guardar los datos en un archivo JSON local
    with open('peliculas_extraidas.json', 'w', encoding='utf-8') as json_file:
        json.dump(movie_data, json_file, ensure_ascii=False, indent=4)

    print("Datos guardados en peliculas_extraidas.json")
else:
    print(f"Error al acceder al archivo: {response.status_code}")
