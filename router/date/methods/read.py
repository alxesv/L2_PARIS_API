from database import session
from router.date.date import router
from models import Date


@router.get("/")
def read_unites(skip: int = 0, limit: int = 10, sort: str = None):
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
        data = session.query(Date).order_by(sort).all()
        if url[-1] != "?":
            url += "&"
        url += f"sort={sort_url}"
    else:
        data = session.query(Date).all()

    if len(data) == 0:
        return {"message": "Aucune date trouvée", "status": 404}

    if skip >= len(data):
        return {"message": "Skip est plus grand que le nombre de date", "status": 400}

    if limit > len(data):
        limit = len(data)

    if url[-1] != "?":
        url += "&"

    response = {"status": 200, "dates": [date.date for date in data[skip:skip + limit]]}

    if skip + limit < len(data):
        response["nextPage"] = f"{url}skip={str(skip + limit)}&limit={str(limit)}"
    if skip > 0:
        response["previousPage"] = f"{url}skip={str(skip - limit)}&limit={str(limit)}"

    return response

@router.get("/{datetime}")
def read_unite(datetime: str):
    """
    Récupère une ligne de la table date
    ### Paramètres
    - date: le nom de la date
    ### Retour
    - un objet de type Date
    - un message d'erreur en cas d'erreur
    - un status code correspondant
    """

    data = session.query(Date).filter(Date.date == datetime).first()

    if not data:
        return {"message": "Date introuvable", "status": 404}

    return {"status": 200, "date": data.date}