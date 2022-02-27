from flask import Flask, render_template, request
import requests
import json
import math
from functions import get_films_names
from time import time
app = Flask(__name__)

@app.route('/', defaults={'page': ''})
@app.route('/<int:page>')
def index(page):
    t1 = time()
    res = requests.get("https://swapi.dev/api/people?page=" + str(page))
    data = json.loads(res.content)
    pages = math.ceil(data["count"] / 10 + (data['count']%10!=0))
    t2 = time()
    time_elapsed = t2 - t1
    print('Main Function Time = ', time_elapsed)
    return render_template("index.html", pages=int(pages), characters = data["results"])



@app.route('/getData', methods=['POST'])
def getData():
    if request.method == 'POST':
        char= request.form["character"].lower()
        res = requests.get("https://swapi.dev/api/people")
        data = json.loads(res.content)
        character = None
        species = None
        filmList = None
        while character == None :
            for result in data["results"]:
                if result["name"].lower() == char:
                    character = result
                    home = requests.get(character["homeworld"])
                    homeWorld = json.loads(home.content)
                    if len(character["species"]) > 0:
                        spec = requests.get(character["species"][0])
                        species = json.loads(spec.content)
                    filmList = get_films_names(character['films'])
                    break
                        
            if character == None:
                if data["next"] == None:
                    warning = "there is no character with this name."
                    return render_template("characters.html", warning=warning)
                res = requests.get(data["next"])
                data = json.loads(res.content)
        print(filmList)
        return render_template("characters.html", 
        character=character, 
        films=filmList if filmList else None,
        species=species["name"] if species else None, 
        homeWorld=homeWorld)
    else :
        return render_template("index.html")

if __name__ == '__main__':
    app.debug = True
    app.run()