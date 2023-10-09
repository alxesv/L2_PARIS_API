import json

from fastapi import FastAPI

from router.weather import router

app = FastAPI()


@router.get('')
def read_json():
    """
    ### Return with this method
    - returns a set of weather data without parameters in the url
    """
    with open("rdu-weather-history.json", "r") as f:
        data = json.load(f)
    return data