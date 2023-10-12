from fastapi import HTTPException
from database import session
from router.parcelle.parcelle import router
from models import Parcelle


@router.get("/", status_code=201)
def read_parcelles(skip: int = 0, limit: int = 10, sort: str = None, no_parcelle:int=None, surface:int=None, nom_parcelle:str=None, coordonnees:str=None):
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
    data = session.query(Parcelle).all()

    url = f"http://127.0.0.1:8000/parcelle?"

    sortable = Parcelle.__table__.columns.keys()

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
                sort_criteria.append(getattr(Parcelle, s[1:]).desc())
                sort_url += f"-{s[1:]},"
            else:
                sort_criteria.append(getattr(Parcelle, s))
                sort_url += f"{s},"
        if url[-1] != "?":
            url += "&"
        url += f"sort={sort_url[:-1]}"
        data = session.query(Parcelle).order_by(*sort_criteria).all()



    if surface is not None and surface > 0:
        if not any(parcelle.surface >= surface for parcelle in data):
            raise HTTPException(status_code=404, detail="Aucune parcelle trouvé avec surface")
        data = [parcelle for parcelle in data if parcelle.surface >= surface]

    if no_parcelle is not None:
        if not any(parcelle.no_parcelle == no_parcelle for parcelle in data):
            raise HTTPException(status_code=404, detail="Aucune parcelle trouvé avec no_parcelle")
        data = [parcelle for parcelle in data if parcelle.no_parcelle == no_parcelle]

    if coordonnees is not None:
        if not any(parcelle.coordonnees == coordonnees for parcelle in data):
            raise HTTPException(status_code=404, detail="Aucune parcelle trouvée avec coordonnees")
        data = [parcelle for parcelle in data if parcelle.coordonnees == coordonnees]
    if nom_parcelle is not None:
        if not any(parcelle.nom_parcelle == nom_parcelle for parcelle in data):
            raise HTTPException(status_code=404, detail="Aucune parcelle trouvée avec nom_parcelle")
        data = [parcelle for parcelle in data if parcelle.nom_parcelle == nom_parcelle]

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