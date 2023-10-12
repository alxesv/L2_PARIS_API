from database import session
from router.posseder.posseder import router
from models import Posseder
from fastapi import HTTPException, status

@router.get("/", status_code=status.HTTP_200_OK)
def read_posseder(skip: int = 0, limit: int = 10, sort: str = None, id_engrais: int = None, code_element: str = None, valeur: int = None):
    """
    Récupère  les lignes de la table posseder
    ### Paramètres
    - skip: nombre de lignes à sauter
    - limit: nombre de lignes à récupérer
    - sort: le ou les champs sur lequel trier les résultats
    - id_engrais: le nom de l'engrais à filtrer
    - code_element: le code de l'élément à filtrer
    - valeur : la valeur à filtrer
    ### Retour
    - un objet JSON contenant  les lignes de la table posseder, filtrées et/ou triées
    - un status code correspondant
    """
    data = session.query(Posseder).all()

    url = f"http://127.0.0.1:8000/posseder?"

    sortable = Posseder.__table__.columns.keys()

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
                raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=f"Le champ de tri {check_sort} n'existe pas")
            if s[0] == "-":
                sort_criteria.append(getattr(Posseder, s[1:]).desc())
                sort_url += f"-{s[1:]},"
            else:
                sort_criteria.append(getattr(Posseder, s))
                sort_url += f"{s},"
        if url[-1] != "?":
            url += "&"
        url += f"sort={sort_url[:-1]}"
        data = session.query(Posseder).order_by(*sort_criteria).all()

    if id_engrais is not None:
        if not any(posseder.id_engrais == id_engrais for posseder in data):
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Engrais non trouvé")
        data = [posseder for posseder in data if posseder.id_engrais == id_engrais]

    if code_element is not None:
        if not any(posseder.code_element == code_element for posseder in data):
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Code de l'élément non trouvé")
        data = [posseder for posseder in data if posseder.code_element == code_element]

    if valeur is not None and valeur > 0:
        if not any(posseder.valeur >= valeur for posseder in data):
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Valeur non trouvée")
        data = [posseder for posseder in data if posseder.valeur >= valeur]

    if len(data) == 0:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Aucune possession trouvée")

    if skip >= len(data):
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Skip est plus grand que le nombre de possession")

    if limit > len(data):
        limit = len(data)

    if url[-1] != "?":
        url += "&"

    response = {"posseders": data[skip:skip + limit]}

    if skip + limit < len(data):
        response["nextPage"] = f"{url}skip={str(skip + limit)}&limit={str(limit)}"
    if skip > 0:
        response["previousPage"] = f"{url}skip={str(skip - limit)}&limit={str(limit)}"

    return response