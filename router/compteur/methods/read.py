from database import session
from router.compteur.compteur import router
from models import Compteur
from sqlalchemy import asc, desc
from fastapi import HTTPException, status


@router.get("/", status_code=status.HTTP_200_OK)
def read_compteurs(skip: int = 0, limit: int = 10, sort: str = None, methode: str = None, route: str = None):
    """
    Récupère les lignes de la table compteur
    ### Paramètres
    - skip: nombre d'éléments à sauter
    - limit: nombre d'éléments à retourner
    - sort: champs à trier
    ### Retour
    - un tableau d'objets de type Compteur
    - un message d'erreur en cas d'erreur
    - un status code correspondant
    """
    url = f"http://127.0.0.1:8000/api/compteur?"

    data = session.query(Compteur).all()

    sortable = Compteur.__table__.columns.keys()

    if sort is not None:
        sort_criteria = []
        sort_url = ""
        sort = sort.split(",")
        for s in sort:
            if s[0] == "-":
                check_sort = s[1:]
            else:
                check_sort = s
            if check_sort not in sortable:
                raise HTTPException(status_code=400, detail=f"Le champ de tri {check_sort} n'existe pas")
            if s[0] == "-":
                sort_criteria.append(getattr(Compteur, s[1:]).desc())
                sort_url += f"-{s[1:]},"
            else:
                sort_criteria.append(getattr(Compteur, s))
                sort_url += f"{s},"
        if url[-1] != "?":
            url += "&"
        url += f"sort={sort_url[:-1]}"
        data = session.query(Compteur).order_by(*sort_criteria).all()

    if methode is not None:
        methode = methode.upper()
        if not any(compteur.methode == methode for compteur in data):
            raise HTTPException(status_code=404, detail="Methode non trouvée")
        data = [compteur for compteur in data if compteur.methode == methode]

    if route is not None:
        if not any(compteur.route.split("/")[2] == route for compteur in data):
            raise HTTPException(status_code=404, detail="Route non trouvée")
        data = [compteur for compteur in data if compteur.route.split("/")[2] == route]

    if len(data) == 0:
        raise HTTPException(status_code=404, detail="Aucun engrais trouvé")

    if skip >= len(data):
        raise HTTPException(status_code=400, detail="Skip est plus grand que le nombre d'engrais")

    if limit > len(data):
        limit = len(data)

    if url[-1] != "?":
        url += "&"

    response = {"compteur": data[skip:skip + limit]}

    if skip + limit < len(data):
        response["nextPage"] = f"{url}skip={str(skip + limit)}&limit={str(limit)}"
    if skip > 0:
        response["previousPage"] = f"{url}skip={str(skip - limit)}&limit={str(limit)}"
    return response
