from database import session
from router.unite.unite import router
from models import Unite


@router.get("/")
def read_unites(skip: int = 0, limit: int = 10, sort: str = None):
    """
    ### Paramètres
    - skip: nombre d'éléments à sauter
    - limit: nombre d'éléments à retourner
    ### Retour
    - un tableau d'objets de type Unite
    - un message d'erreur en cas d'erreur
    - un status code correspondant
    """

    url = f"http://127.0.0.1:8000/unite?"

    if sort and sort in ["un", "-un"]:
        sort_url = ""
        if sort[0] == "-":
            sort_url += f"{sort}"
            sort = getattr(Unite, sort[1:]).desc()
        else:
            sort_url += f"{sort}"
            sort = getattr(Unite, sort)
        data = session.query(Unite).order_by(sort).all()
        if url[-1] != "?":
            url += "&"
        url += f"sort={sort_url}"
    else:
        data = session.query(Unite).all()

    if len(data) == 0:
        return {"message": "Aucune unite trouvée", "status": 404}

    if skip >= len(data):
        return {"message": "Skip est plus grand que le nombre d'unite", "status": 400}

    if limit > len(data):
        limit = len(data)

    if url[-1] != "?":
        url += "&"

    response = {"status": 200, "unites": [un.un for un in data[skip:skip + limit]]}

    if skip + limit < len(data):
        response["nextPage"] = f"{url}skip={str(skip + limit)}&limit={str(limit)}"
    if skip > 0:
        response["previousPage"] = f"{url}skip={str(skip - limit)}&limit={str(limit)}"

    return response

@router.get("/{unite}")
def read_unite(unite: str):
    """
    ### Paramètres
    - unite: le nom de l'unite
    ### Retour
    - un objet de type Unite
    - un message d'erreur en cas d'erreur
    - un status code correspondant
    """

    data = session.query(Unite).filter(Unite.un == unite).first()

    if not data:
        return {"message": "Unite introuvable", "status": 404}

    return {"status": 200, "unite": data.un}