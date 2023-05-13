import requests
from bs4 import BeautifulSoup
import os
import csv

# Función para crear una carpeta si no existe
def create_folder(folder_name):
    if not os.path.exists(folder_name):
        os.makedirs(folder_name)

# Función para descargar y guardar una imagen en una carpeta
def save_image(image_url, file_name, folder_name):
    response = requests.get(image_url)
    with open(f"{folder_name}/{file_name}", "wb") as f:
        f.write(response.content)

# Función para guardar los datos de las películas en un archivo CSV
def save_movies_data(movies, file_name):
    with open(file_name, mode='w', newline='') as csv_file:
        fieldnames = ['Rank', 'Title', 'Year', 'Rating', 'Image URL']
        writer = csv.DictWriter(csv_file, fieldnames=fieldnames)

        writer.writeheader()
        for movie in movies:
            writer.writerow(movie)

# Hacer una solicitud HTTP a la página de las 10 mejores películas de todos los tiempos de IMDb
url = 'https://www.imdb.com/chart/top/'
response = requests.get(url)

# Analizar el HTML de la página web para encontrar las películas
soup = BeautifulSoup(response.text, 'html.parser')
movie_table = soup.find('table', class_='chart full-width')
movie_rows = movie_table.find_all('tr')

# Crear una lista para almacenar los datos de cada película
movies = []

# Crear una carpeta para las imágenes si no existe
create_folder("imagenesweb")

# Iterar sobre cada fila de la tabla de películas y extraer los datos necesarios
for row in movie_rows:
    cells = row.find_all('td')
    if len(cells) > 1:
        rank = cells[0].text.strip()
        title = cells[1].a.text.strip()
        year = cells[1].span.text.strip('()')
        rating = cells[2].strong.text.strip()
        image_url = cells[0].img['src']
        
        # Guardar la imagen en la carpeta "imagenesweb"
        save_image(image_url, f"{title}.jpg", "imagenesweb")
                
        # Agregar los datos de la película a la lista de películas
        movies.append({
            'Rank': rank,
            'Title': title,
            'Year': year,
            'Rating': rating,
            'Image URL': image_url,
        })

# Guardar los datos de las películas en un archivo CSV
save_movies_data(movies, 'movies.csv')
