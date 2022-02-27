import requests
import json

def index(page):
    t1 = time()
    res = requests.get("https://swapi.dev/api/people?page=" + str(page))
    data = json.loads(res.content)
    pages = math.ceil(data["count"] / 10 + (data['count']%10!=0))
    t2 = time()
    time_elapsed = t2 - t1
    print('Main Function Time = ', time_elapsed)
    return render_template("index.html", pages=int(pages), characters = data["results"])

