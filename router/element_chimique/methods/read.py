from database import session
from router.element_chimique.element_chimique import router
from models import ElementChimique
from sqlalchemy import asc, desc
from fastapi import HTTPException, status


@router.get("/", status_code=status.HTTP_200_OK)
def read_element_chimiques(skip: int = 0, limit: int = 10, sort: str = None, un: str = None, libelle_element: str = None):
    """
    Récupère les lignes de la table élément chimique
    ### Paramètres
    - skip: nombre d'éléments à sauter
    - limit: nombre d'éléments à retourner
    ### Retour
    - un tableau d'objets de type ElementChimique
    - un message d'erreur en cas d'erreur
    - un status code correspondant
    """

    url = f"http://127.0.0.1:8000/element_chimique?"

    sort_mapping = ElementChimique.__table__.columns.keys()

    if sort:
        sort_fields = sort.split(',')
        sort_criteria = []

        for field in sort_fields:
            if field.startswith('-'):
                sort_criteria.append(desc(sort_mapping[field[1:]]))
            else:
                sort_criteria.append(asc(sort_mapping[field]))

        data = session.query(ElementChimique).order_by(*sort_criteria).all()
    else:
        data = session.query(ElementChimique).all()

    if un is not None:
        if not any(element_chimique.un == un for element_chimique in data):
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Unite non trouvée")
        data = [element_chimique for element_chimique in data if element_chimique.un == un]

    if libelle_element is not None:
        if not any(element_chimique.libelle_element == libelle_element for element_chimique in data):
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Aucun libellé trouvée")
        data = [element_chimique for element_chimique in data if element_chimique.libelle_element == libelle_element]

    if len(data) == 0:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Aucun élément chimique trouvée")

    if skip >= len(data):
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=f"Skip est plus grand que le nombre d'élément chimique ({len(data)})")

    if limit > len(data):
        limit = len(data)

    if url[-1] != "?":
        url += "&"

    response = { "elements": [element_chimique for element_chimique in data[skip:skip + limit]] }

    if skip + limit < len(data):
        response["nextPage"] = f"{url}skip={str(skip + limit)}&limit={str(limit)}"
    if skip > 0:
        response["previousPage"] = f"{url}skip={str(skip - limit)}&limit={str(limit)}"

    return response


@router.get("/{code_element}", status_code=status.HTTP_200_OK)
def read_element_chimique(code_element: str):
    """
    Récupère une ligne de la table élément chimique
    ### Paramètres
    - code_element: Le code de l'élément chimique
    ### Retour
    - un objet de type ElementChimique
    - un message d'erreur en cas d'erreur
    - un status code correspondant
    """

    data = session.query(ElementChimique).filter(ElementChimique.code_element == code_element).first()

    if not data:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Élément introuvable")

    return { "element_chimique": data }