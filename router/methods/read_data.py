import json

from fastapi import FastAPI

from router.weather import router

app = FastAPI()


@router.get("/")
def read_json(skip: int = 0, limit: int = 10, date: str = None, tmin: int = None, tmax: int = None, prcp: float = None,
              snow: float = None, snwd: float = None, awnd: float = None, sort: str = None):
    """
    ### Parameters
    - skip: number of elements to skip
    - limit: number of elements to return
    - date: date of the weather data
    - tmin: minimum temperature
    - tmax: maximum temperature
    - prcp: minimum precipitation rate
    - snow: minimum snow rate
    - snwd: minimum snow depth
    - awnd: minimum wind rate
    ### Return
    - a set of weather data, filtered by the parameters, with the next and previous pages if needed
    - a message if no data is found
    - an appropriate status code
    """

    with open("rdu-weather-history.json", "r") as f:
        data = json.load(f)

    url = f"http://127.0.0.1:8000/weather?"

    if date is not None:
        data = [w for w in data if w["date"] == date]
        if url[-1] != "?":
            url += "&"
        url += f"date={date}"
    if tmin is not None:
        data = [w for w in data if w["tmin"] >= tmin]
        if url[-1] != "?":
            url += "&"
        url += f"tmin={tmin}"
    if tmax is not None:
        data = [w for w in data if w["tmax"] <= tmax]
        if url[-1] != "?":
            url += "&"
        url += f"tmax={tmax}"
    if prcp is not None:
        data = [w for w in data if w["prcp"] >= prcp]
        if url[-1] != "?":
            url += "&"
        url += f"prcp={prcp}"
    if snow is not None:
        data = [w for w in data if w["snow"] >= snow]
        if url[-1] != "?":
            url += "&"
        url += f"snow={snow}"
    if snwd is not None:
        data = [w for w in data if w["snwd"] >= snwd]
        if url[-1] != "?":
            url += "&"
        url += f"snwd={snwd}"
    if awnd is not None:
        data = [w for w in data if w["awnd"] >= awnd]
        if url[-1] != "?":
            url += "&"
        url += f"awnd={awnd}"

    if sort is not None:
        sort_url = ""
        sort = sort.split(",")
        for s in sort:
            if s[0] == "-":
                data = sorted(data, key=lambda x: x[s[1:]], reverse=True)
                sort_url += f"-{s[1:]},"
            else:
                data = sorted(data, key=lambda x: x[s])
                sort_url += f"{s},"
        if url[-1] != "?":
            url += "&"
        url += f"sort={sort_url[:-1]}"


    if len(data) == 0:
        return {"status": 404, "message": "No data found"}

    if skip > len(data):
        return {"status": 400, "message": "Skip is greater than the number of data"}

    if url[-1] != "?":
        url += "&"
    response = {"status": 201, "data": data[skip:skip + limit]}
    if skip + limit < len(data):
        response["nextPage"] = f"{url}skip={str(skip + limit)}&limit={str(limit)}"
    if skip > 0:
        response["previousPage"] = f"{url}skip={str(skip - limit)}&limit={str(limit)}"
    return response
