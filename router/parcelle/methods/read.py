from fastapi import HTTPException
from database import session
from router.parcelle.parcelle import router
from models import Parcelle


@router.get("/", status_code=201)
def read_parcelles(skip: int = 0, limit: int = 10, sort: str = None):
    """
    Récupère les lignes de la table parcelle
    ### Paramètres
    - skip: nombre d'éléments à sauter
    - limit: nombre d'éléments à retourner
    ### Retour
    - un tableau d'objets de type Parcelle
    - un message d'erreur en cas d'erreur
    - un status code correspondant
    """

    url = f"http://127.0.0.1:8000/parcelle?"

    if sort and sort in ["no_parcelle", "-no_parcelle"]:
        sort_url = ""
        if sort[0] == "-":
            sort_url += f"{sort}"
            sort = getattr(Parcelle, sort[1:]).desc()
        else:
            sort_url += f"{sort}"
            sort = getattr(Parcelle, sort)
        data = session.query(Parcelle).order_by(sort).all()
        if url[-1] != "?":
            url += "&"
        url += f"sort={sort_url}"
    else:
        data = session.query(Parcelle).all()

    if len(data) == 0:
        raise HTTPException(status_code=404,detail="Aucune parcelle trouvée")


    if skip >= len(data):
        raise HTTPException(status_code=400, detail="Skip est plus grand que le nombre de parcelle")

    if limit > len(data):
        limit = len(data)

    if url[-1] != "?":
        url += "&"

    response = {"parcelles": [no_parcelle for no_parcelle in data[skip:skip + limit]]}

    if skip + limit < len(data):
        response["nextPage"] = f"{url}skip={str(skip + limit)}&limit={str(limit)}"
    if skip > 0:
        response["previousPage"] = f"{url}skip={str(skip - limit)}&limit={str(limit)}"

    return response

@router.get("/{parcelle}", status_code=201)
def read_parcelle(parcelle: int):
    """
    Récupère une ligne de la table parcelle
    ### Paramètres
    - no_parcelle: l'id de parcelle'
    ### Retour
    - un objet de type Parcelle
    - un message d'erreur en cas d'erreur
    - un status code correspondant
    """

    data = session.query(Parcelle).filter(Parcelle.no_parcelle == parcelle).first()

    if not data:
        raise HTTPException(status_code=404, detail="Parcelle introuvable")

    return {"parcelle": data}