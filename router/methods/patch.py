from typing import Union
import json

from fastapi import status, HTTPException
from router.weather import router


@router.patch("/", status_code=status.HTTP_200_OK)
def modify_weather(
    date: str,
    tmin: int | None = None,
    tmax: int | None = None,
    prcp: float | None = None,
    snow: float | None = None,
    snwd: float | None = None,
    awnd: float | None = None,
):
    """
    Modify a weather forecast based on one/multiple parameters
    ### Parameters
    - date: Date of the forecast (identifier)
    - tmin: Minimum temperature (optionnal)
    - tmax: Maximum temperature (optionnal)
    - prcp: Precipitation rate (optionnal)
    - snow: Snow rate (optionnal)
    - snwd: Snow depth (optionnal)
    - awnd: Wind rate (optionnal)
    ### Return
    - JSON with the modified weather forecast
    """
    with open("../../rdu-weather-history.json", "r") as json_file:
        data = json.load(json_file)

    matching_items = [item for item in data if item.get("date") == date]

    if len(matching_items) == 0:
        raise HTTPException(status_code=404, detail="Forecast with that date doesn't exist.")

    matching_item = matching_items[0]
    matching_item['tmin'] = tmin if tmin is not None else matching_item['tmin']
    matching_item['tmax'] = tmax if tmax is not None else matching_item['tmax']
    matching_item['prcp'] = prcp if prcp is not None else matching_item['prcp']
    matching_item['snow'] = snow if snow is not None else matching_item['snow']
    matching_item['snwd'] = snwd if snwd is not None else matching_item['snwd']
    matching_item['awnd'] = awnd if awnd is not None else matching_item['awnd']

    with open("../../rdu-weather-history.json", "w") as json_file:
        json.dump(data, json_file)

    return {'forecast': matching_item}
