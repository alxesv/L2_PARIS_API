from database import session
from router.production.production import router
from models import Production
from fastapi import status, HTTPException
from sqlalchemy import asc, desc


@router.get("/", status_code=status.HTTP_200_OK)
def read_productions(skip: int = 0, limit: int = 10, sort: str = None, un: str = None, nom_production: str = None):
    """
    Récupère les lignes de la table production
    ### Paramètres
    - skip: nombre d'éléments à sauter
    - limit: nombre d'éléments à retourner
    ### Retour
    - un tableau d'objets de type Production
    - un message d'erreur en cas d'erreur
    - un status code correspondant
    """

    url = f"http://127.0.0.1:8000/production?"

    data = session.query(Production).all()

    sortable = Production.__table__.columns.keys()

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
                sort_criteria.append(getattr(Production, s[1:]).desc())
                sort_url += f"-{s[1:]},"
            else:
                sort_criteria.append(getattr(Production, s))
                sort_url += f"{s},"
        if url[-1] != "?":
            url += "&"
        url += f"sort={sort_url[:-1]}"
        data = session.query(Production).order_by(*sort_criteria).all()

    if un is not None:
        if not any(production.un == un for production in data):
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Unite non trouvée")
        data = [production for production in data if production.un == un]

    if nom_production is not None:
        if not any(production.nom_production == nom_production for production in data):
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Aucune production trouvée")
        data = [production for production in data if production.nom_production == nom_production]

    if len(data) == 0:
        raise HTTPException(status_code=400, detail="Aucune production trouvée")

    if skip >= len(data):
        raise HTTPException(status_code=400, detail="Skip est plus grand que le nombre de production")

    if limit > len(data):
        limit = len(data)

    if url[-1] != "?":
        url += "&"

    response = {"productions": [{"code_production": data.code_production, "un": data.un, "nom_production": data.nom_production} for data in data[skip:skip + limit]]}

    if skip + limit < len(data):
        response["nextPage"] = f"{url}skip={str(skip + limit)}&limit={str(limit)}"
    if skip > 0:
        response["previousPage"] = f"{url}skip={str(skip - limit)}&limit={str(limit)}"

    return response

@router.get("/{code_production}", status_code=status.HTTP_200_OK)
def read_code_production(code_production: int):
    """
    Récupère une ligne de la table production
    ### Paramètres
    - unite: le nom de l'unite de la production
    ### Retour
    - un objet de type Production
    - un message d'erreur en cas d'erreur
    - un status code correspondant
    """

    data = session.query(Production).filter(Production.code_production == code_production).first()

    if not data:
        raise HTTPException(status_code=404, detail="Unite introuvable")

    return {"production": data}