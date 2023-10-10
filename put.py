from router.weather import router
import json
@router.put("/")
def put_weather(
    date: str,
    tmin: int,
    tmax: int,
    prcp: float,
    snow: float,
    snwd: float,
    awnd: float,
):
    """
    Replace all the parameters of a weather
    ### Parameters
    - date: Date of the forecast (identifier)
    - tmin: Minimum temperature (required)
    - tmax: Maximum temperature (required)
    - prcp: Precipitation rate (required)
    - snow: Snow rate (required)
    - snwd: Snow depth (required)
    - awnd: Wind rate (required)
    ### Return
    - JSON with all the new weather parameters
    """
    with open("rdu-weather-history.json", "r") as json_file:
        data = json.load(json_file)

    matching_items = [item for item in data if item.get("date") == date]

    if len(matching_items) == 0:
        raise HTTPException(status_code=404, detail="Forecast with that date doesn't exist.")

    matching_item = matching_items[0]
    matching_item['tmin'] = tmin
    matching_item['tmax'] = tmax
    matching_item['prcp'] = prcp
    matching_item['snow'] = snow
    matching_item['snwd'] = snwd
    matching_item['awnd'] = awnd

    with open("rdu-weather-history.json", "w") as json_file:
        json.dump(data, json_file)

    return {'status': 200, 'message': 'Weather data replace','forecast': matching_item}