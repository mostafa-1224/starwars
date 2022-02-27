from flask import Flask, render_template, request
import requests
import json
import math
from time import time
app = Flask(__name__)

def get_request(request_url):
        res = requests.get(request_url)
        data = json.loads(res.content)
        return data

def get_films_list(films_urls):
    filmList = []
    for film in films_urls:
        data = get_request(film)
        filmList.append(data)
    return filmList

@app.route('/', defaults={'page': ''})
@app.route('/<int:page>')
def index(page):
    t1 = time()
    request_url = "https://swapi.dev/api/people?page=" + str(page)
    data = get_request(request_url)
    pages = math.ceil(data["count"] / 10 + (data['count']%10 != 0))
    t2 = time()
    time_elapsed = t2 - t1
    print('Main Function Time = ', time_elapsed)
    return render_template("index.html", pages=int(pages), characters = data["results"])


@app.route('/getData', methods=['POST'])
def getData():
    if request.method == 'POST':
        char = request.form["character"].lower()
        request_url = "https://swapi.dev/api/people?search="+char
        species = None
        filmList = None
        homeWorld = None
        fullCharactersInfo = []
        data = get_request(request_url)
        characters = data['results']
        t3 = time()
        for character in characters:
            if len(character["species"]) > 0:
                species = get_request(character["species"][0])
            filmList = get_films_list(character['films'])
            homeWorld = get_request(character["homeworld"])
            fullCharactersInfo.append({"character":character, "filmList":filmList, "species":species, "homeWorld":homeWorld})
        if characters == []:
            warning = "there is no character with this name."
            return render_template("characters.html", warning = warning)
        else:
            t4 = time()
            time_elapsed = t4 - t3
            print('Main Function Time = ', time_elapsed)
            return render_template(
                "characters.html", 
                fullCharactersInfo = fullCharactersInfo, 
            )
    else :
        return render_template("index.html")

if __name__ == '__main__':
    app.debug = True
    app.run()