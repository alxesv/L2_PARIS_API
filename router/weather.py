from fastapi import APIRouter
from fastapi import FastAPI
import json
router = APIRouter(prefix="/weather", tags=['weather'])

@router.get('')
def read_json():
    """
    ### Return with this method
    - returns a set of weather data without parameters in the url
    """
    with open("rdu-weather-history.json", "r") as f:
        data = json.load(f)
    return data