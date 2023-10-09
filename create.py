from router.weather import router
from pydantic import BaseModel
import datetime
import json
class Weather(BaseModel):
    date: str
    tmin: int
    tmax: int
    prcp: float
    snow: float
    snwd: float
    awnd: float


@router.post("/")
def create_weather(weather: Weather):
    """
    Ajoute une ligne dans la table weather
    ### Paramètres
    - weather: objet de type Weather, avec les champs date, tmin, tmax, prcp, snow, snwd, awnd
    ### Retour
    - Status code 200 si tout s'est bien passé avec message "Weather ajouté" et le weather ajouté
    - Message d'erreur avec le status code correspondant sinon
    """
    try:
        datetime.date.fromisoformat(weather.date)
    except ValueError:
        return {"status": 422, "message": "Date invalide"}

    if weather.date in [w["date"] for w in json.load(open("rdu-weather-history.json", "r"))]:
        return {"status": 400, "message": "Date déjà présente dans la base"}

    if weather.tmin > weather.tmax:
        return {"status": 400, "message": "Tmin doit être inférieur à Tmax"}

    with open("rdu-weather-history.json", "r") as f:
        data = json.load(f)
        data.append(weather.model_dump())
    with open("rdu-weather-history.json", "w") as f:
        json.dump(data, f)

    return {"status": 200, "message": "Weather ajouté", "weather": weather.model_dump()}