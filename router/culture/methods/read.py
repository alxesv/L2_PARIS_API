from sqlalchemy.orm import lazyload, joinedload

from database import session
from router.culture.culture import router
from models import Culture
from sqlalchemy import asc, desc
from fastapi import HTTPException, status


@router.get("/", status_code=status.HTTP_200_OK)
def read_cultures(skip: int = 0, limit: int = 10, sort: str = None):
    """
    Récupère les lignes de la table élément chimique
    ### Paramètres
    - skip: nombre d'éléments à sauter
    - limit: nombre d'éléments à retourner
    ### Retour
    - un tableau d'objets de type Culture
    - un message d'erreur en cas d'erreur
    - un status code correspondant
    """

    url = f"http://127.0.0.1:8000/culture?"

    sort_mapping = Culture.__table__.columns.keys()

    if sort:
        sort_fields = sort.split(',')
        sort_criteria = []

        for field in sort_fields:
            if field.startswith('-'):
                sort_criteria.append(desc(sort_mapping[field[1:]]))
            else:
                sort_criteria.append(asc(sort_mapping[field]))

        data = (session.query(Culture).order_by(*sort_criteria)
                .options(joinedload(Culture.parcelle), joinedload(Culture.production)).all())
    else:
        data = (session.query(Culture)
                .options(joinedload(Culture.parcelle), joinedload(Culture.production)).all())

    if len(data) == 0:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Aucune culture trouvée")

    if skip >= len(data):
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=f"Skip est plus grand que le nombre de culture ({len(data)})")

    if limit > len(data):
        limit = len(data)

    if url[-1] != "?":
        url += "&"

    response = { "cultures": [culture for culture in data[skip:skip + limit]] }

    if skip + limit < len(data):
        response["nextPage"] = f"{url}skip={str(skip + limit)}&limit={str(limit)}"
    if skip > 0:
        response["previousPage"] = f"{url}skip={str(skip - limit)}&limit={str(limit)}"

    return response


@router.get("/{identifiant_culture}", status_code=status.HTTP_200_OK)
def read_culture(identifiant_culture: int):
    """
    Récupère une ligne de la table élément chimique
    ### Paramètres
    - identifiant_culture: Identifiant de la culture voulue
    ### Retour
    - un objet de type Culture
    - un message d'erreur en cas d'erreur
    - un status code correspondant
    """

    data = (session.query(Culture).filter(Culture.identifiant_culture == identifiant_culture)
            .options(joinedload(Culture.parcelle), joinedload(Culture.production)).first())

    if not data:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Culture introuvable")

    return { "culture": data }