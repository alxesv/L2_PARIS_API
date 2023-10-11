from database import session
from router.unite.unite import router
from models import Unite
from fastapi import HTTPException

@router.get("/", status_code=200)
def read_unites(skip: int = 0, limit: int = 10, sort: str = None):
    """
    Récupère les lignes de la table unite
    ### Paramètres
    - skip: nombre d'éléments à sauter
    - limit: nombre d'éléments à retourner
    ### Retour
    - un tableau d'objets de type Unite
    - un message d'erreur en cas d'erreur
    - un status code correspondant
    - url de navigation pour la pagination
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
        raise HTTPException(status_code=404, detail="Aucune unite trouvée")

    if skip >= len(data):
        raise HTTPException(status_code=400, detail="Skip est plus grand que le nombre d'unite")

    if limit > len(data):
        limit = len(data)

    if url[-1] != "?":
        url += "&"

    response = {"unites": [un.un for un in data[skip:skip + limit]]}

    if skip + limit < len(data):
        response["nextPage"] = f"{url}skip={str(skip + limit)}&limit={str(limit)}"
    if skip > 0:
        response["previousPage"] = f"{url}skip={str(skip - limit)}&limit={str(limit)}"

    return response

@router.get("/{unite}", status_code=200)
def read_unite(unite: str):
    """
    Récupère une ligne de la table unite
    ### Paramètres
    - unite: le nom de l'unite
    ### Retour
    - un objet de type Unite
    - un message d'erreur en cas d'erreur
    - un status code correspondant
    """

    data = session.query(Unite).filter(Unite.un == unite).first()

    if not data:
        raise HTTPException(status_code=404, detail="Unite non trouvée")

    return {"unite": data.un}