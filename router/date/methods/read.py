from database import session
from router.date.date import router
from models import Date
from fastapi import HTTPException
from sqlalchemy.orm import joinedload


@router.get("/",status_code=200)
def read_dates(skip: int = 0, limit: int = 10, sort: str = None):
    """
    Récupère les lignes de la table date
    ### Paramètres
    - skip: nombre d'éléments à sauter
    - limit: nombre d'éléments à retourner
    ### Retour
    - un tableau d'objets de type Date
    - un message d'erreur en cas d'erreur
    - un status code correspondant
    """

    url = f"http://127.0.0.1:8000/date?"

    if sort and sort in ["date", "-date"]:
        sort_url = ""
        if sort[0] == "-":
            sort_url += f"{sort}"
            sort = getattr(Date, sort[1:]).desc()
        else:
            sort_url += f"{sort}"
            sort = getattr(Date, sort)
        data = session.query(Date).order_by(sort).options(joinedload(Date.epandres)).all()
        if url[-1] != "?":
            url += "&"
        url += f"sort={sort_url}"
    else:
        data = session.query(Date).options(joinedload(Date.epandres)).all()

    if len(data) == 0:
        raise HTTPException(status_code=404,detail="Aucune date trouvée")

    if skip >= len(data):
        raise HTTPException(status_code=400, detail="Skip est plus grand que le nombre de date")

    if limit > len(data):
        limit = len(data)

    if url[-1] != "?":
        url += "&"

    response = {"dates": data[skip:skip + limit]}

    if skip + limit < len(data):
        response["nextPage"] = f"{url}skip={str(skip + limit)}&limit={str(limit)}"
    if skip > 0:
        response["previousPage"] = f"{url}skip={str(skip - limit)}&limit={str(limit)}"

    return response

@router.get("/{datetime}",status_code=200)
def read_date(datetime: str):
    """
    Récupère une ligne de la table date
    ### Paramètres
    - date: le nom de la date
    ### Retour
    - un objet de type Date
    - un message d'erreur en cas d'erreur
    - un status code correspondant
    """

    data = session.query(Date).filter(Date.date == datetime).options(joinedload(Date.epandres)).first()

    if not data:
        raise HTTPException(status_code=404,detail="Date introuvable")

    return {"date": data.date}