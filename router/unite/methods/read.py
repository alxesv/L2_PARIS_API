from database import session
from router.unite.unite import router
from models import Unite
from fastapi import HTTPException, status
from sqlalchemy.orm import joinedload

@router.get("/", status_code=status.HTTP_200_OK)
def read_unites(skip: int = 0, limit: int = 10, sort: str = None, populate: bool = False):
    """
    Récupère les lignes de la table Unite
    ### Paramètres
    - skip: nombre d'éléments à sauter
    - limit: nombre d'éléments à retourner
    - sort: le ou les champs sur lequel trier les résultats
    ### Retour
    - un objet JSON contenant  les lignes de la table Unite, filtrées et/ou triées
    - un message d'erreur en cas d'erreur
    - un status code correspondant
    - url de navigation pour la pagination
    """
    url = f"http://127.0.0.1:8000/api/unite?"

    sortable = Unite.__table__.columns.keys()

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
                raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                                    detail=f"Le champ de tri {check_sort} n'existe pas")
            if s[0] == "-":
                sort_criteria.append(getattr(Unite, s[1:]).desc())
                sort_url += f"-{s[1:]},"
            else:
                sort_criteria.append(getattr(Unite, s))
                sort_url += f"{s},"
        if populate is not False:
            data = (session.query(Unite).order_by(*sort_criteria)
                    .options(joinedload(Unite.element_chimiques), joinedload(Unite.productions), joinedload(Unite.engrais))
                    .all())
            if url[-1] != "?":
                url += "&"
            url += f"populate=true"
        else:
            data = (session.query(Unite).order_by(*sort_criteria).all())
        if url[-1] != "?":
            url += "&"
        url += f"sort={sort_url[:-1]}"
    else:
        if populate is not False:
            data = (session.query(Unite)
                    .options(joinedload(Unite.element_chimiques), joinedload(Unite.productions), joinedload(Unite.engrais))
                    .all())
            if url[-1] != "?":
                url += "&"
            url += f"populate=true"
        else:
            data = (session.query(Unite).all())

    if len(data) == 0:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Aucune unite trouvée")

    if skip >= len(data):
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Skip est plus grand que le nombre d'unite")

    if limit > len(data):
        limit = len(data)

    if url[-1] != "?":
        url += "&"

    response = {"unites": data[skip:skip + limit]}

    if skip + limit < len(data):
        response["nextPage"] = f"{url}skip={str(skip + limit)}&limit={str(limit)}"
    if skip > 0:
        response["previousPage"] = f"{url}skip={str(skip - limit)}&limit={str(limit)}"

    return response

@router.get("/{unite}", status_code=status.HTTP_200_OK)
def read_unite_by_unite(unite: str, populate: bool = False):
    """
    Récupère une ligne de la table Unite
    ### Paramètres
    - unite: le nom de l'unite
    ### Retour
    - un objet de type Unite
    - un message d'erreur en cas d'erreur
    - un status code correspondant
    """

    if populate is not False:
        data = (session.query(Unite).filter(Unite.un == unite)
                .options(joinedload(Unite.element_chimiques), joinedload(Unite.productions), joinedload(Unite.engrais))
                .first())
    else:
        data = (session.query(Unite).filter(Unite.un == unite).first())

    if not data:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Unité introuvable")

    return {"unite": data}