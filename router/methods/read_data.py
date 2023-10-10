import json

from fastapi import FastAPI

from router.weather import router

app = FastAPI()


@router.get("/")
def read_json(skip: int = 0, limit: int = 10):
    """
    ### Parameters
    - skip: number of elements to skip
    - limit: number of elements to return
    ### Return
    - a set of weather data, filtered by the parameters
    """

    with open("rdu-weather-history.json", "r") as f:
        data = json.load(f)

    response = {"status": 201, "data": data[skip:skip + limit], "nextPage" : f"http://127.0.0.1:8000/weather?skip={str(skip + limit)}&limit={str(limit)}"}
    if skip > 0:
        response["previousPage"] = f"http://127.0.0.1:8000/weather?skip={str(skip - limit)}&limit={str(limit)}"
    return response
