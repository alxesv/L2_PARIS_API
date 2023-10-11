from database import session
from router.element_chimique.element_chimique import router
from models import ElementChimique
from sqlalchemy import asc, desc


@router.get("/")
def read_element_chimiques(skip: int = 0, limit: int = 10, sort: str = None):
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

    sort_mapping = {
        "code_element": ElementChimique.code_element,
        "un": ElementChimique.un,
        "libelle_element": ElementChimique.libelle_element,
    }

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

    if len(data) == 0:
        return {"message": "Aucun élément chimique trouvée", "status": 404}

    if skip >= len(data):
        return {"message": "Skip est plus grand que le nombre d'élément chimique", "status": 400}

    if limit > len(data):
        limit = len(data)

    if url[-1] != "?":
        url += "&"

    response = {"status": 200, "elements": [element_chimique for element_chimique in data[skip:skip + limit]]}

    if skip + limit < len(data):
        response["nextPage"] = f"{url}skip={str(skip + limit)}&limit={str(limit)}"
    if skip > 0:
        response["previousPage"] = f"{url}skip={str(skip - limit)}&limit={str(limit)}"

    return response

@router.get("/{code_element}")
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
        return {"message": "Élément introuvable", "status": 404}

    return {"status": 200, "element": data}