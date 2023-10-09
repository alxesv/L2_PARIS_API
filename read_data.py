import json

from fastapi import FastAPI

app = FastAPI()

@app.get('')
def read_json():
    """
    ### Retour
    - return un ensemble de données de la date
    mise en paramètre de l'url a la place de {date}
    """
    with open("rdu-weather-history.json", "r") as f:
        data = json.load(f)
    return data