import datetime
from typing import Union
from fastapi import FastAPI

app = FastAPI()



@app.get("/itemsjson/{date}")
def read_data(date: datetime.date,tmin: int,tmax: int,prc: float,snow:float,snwd:float,awnd:float):
    """
    ### Retour
    - return un ensemble de données de la date
    mise en paramètre de l'url a la place de {date}
    """
    return {"date": date, "tmin": tmin,"tmax":tmax,"prc":prc,"snow":snow,"snwd":snwd,"awnd":awnd,}

