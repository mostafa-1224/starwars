import requests
import json

def get_films_names(films_urls):
    filmList = []
    for film in films_urls:
        filmRes = requests.get(film)
        filmList.append(json.loads(filmRes.content))
    return filmList