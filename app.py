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
# Home Page and charachters paginations routes #
@app.route('/', defaults={'page': ''})
@app.route('/<int:page>')
def index(page):
    t1 = time()
    request_url = "https://swapi.dev/api/people?page=" + str(page)
    data = get_request(request_url)
    pages = math.ceil(data["count"] / 10 + (data['count']%10 != 0))
    t2 = time()
    time_elapsed = t2 - t1
    print('Initial Function Time = ', time_elapsed)
    return render_template("index.html", pages=int(pages), characters = data["results"])
##########################################################################################

# Route To Present the search results for all matching characters for one search #  
@app.route('/matched-characters', methods=['POST'])
def getMatchedCharacters():
        t3=time()
        request_url = "https://swapi.dev/api/people?page=1"
        data = get_request(request_url)
        pages = math.ceil(data["count"] / 10 + (data['count']%10 != 0)) 
        char = request.form["character"].lower()
        request_url = "https://swapi.dev/api/people?search="+char
        search_data = get_request(request_url)
        matched_characters = search_data['results']
        while search_data["next"] != None:
            search_data = get_request(search_data['next'])
            for item in search_data['results']:
                matched_characters.append(item)
        t4 = time()
        time_elapsed = t4 - t3
        print("Characters Search Matching Function Time = ", time_elapsed)
        if matched_characters == []:
            warning = "there is no character with this name."
            return render_template("index.html", warning = warning, pages=int(pages), characters = data["results"])
        else:
            return render_template(
            "index.html", 
            matched_characters = matched_characters, pages=int(pages), characters = data["results"]
            )
################################################################################################
@app.route('/character-info/<string:name>')
def getCharacterData(name):
        request_url = "https://swapi.dev/api/people?search="+name
        species = None
        filmList = None
        homeWorld = None
        data = get_request(request_url)
        character=data["results"][0]
        t3 = time()
        if len(character["species"]) > 0:
            species = get_request(character["species"][0])
        filmList = get_films_list(character['films'])
        homeWorld = get_request(character["homeworld"])
        if character == None:
            warning = "there is no character with this name."
            return render_template("characters.html", warning = warning)
        else:
            t4 = time()
            time_elapsed = t4 - t3
            print('Character Info Function Time = ', time_elapsed)
            return render_template(
                "characters.html", 
                character = character,
                homeWorld = homeWorld,
                species = species,
                filmList = filmList
            )

if __name__ == '__main__':
    app.debug = True
    app.run()