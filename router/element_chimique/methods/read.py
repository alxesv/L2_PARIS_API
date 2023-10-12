from database import session
from router.element_chimique.element_chimique import router
from models import ElementChimique
from fastapi import HTTPException, status


@router.get("/", status_code=status.HTTP_200_OK)
def read_element_chimiques(skip: int = 0, limit: int = 10, sort: str = None, un: str = None, libelle_element: str = None):
    """
    Récupère les lignes de la table Element_Chimique
    ### Paramètres
    - skip: nombre d'éléments à sauter
    - limit: nombre d'éléments à retourner
    - un : l'unité de l'élément chimique à filtrer
    - libelle_element: description de l'élément chimique à filtrer
    ### Retour
    - un objet JSON contenant les lignes de la talbe Element_Chimique
    - un message d'erreur en cas d'erreur
    - un status code correspondant
    """
    data = session.query(ElementChimique).all()

    url = f"http://127.0.0.1:8000/element_chimique?"

    sortable = ElementChimique.__table__.columns.keys()

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
                sort_criteria.append(getattr(ElementChimique, s[1:]).desc())
                sort_url += f"-{s[1:]},"
            else:
                sort_criteria.append(getattr(ElementChimique, s))
                sort_url += f"{s},"
        if url[-1] != "?":
            url += "&"
        url += f"sort={sort_url[:-1]}"
        data = session.query(ElementChimique).order_by(*sort_criteria).all()

    if un is not None:
        if not any(element_chimique.un == un for element_chimique in data):
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Aucune unité trouvée")
        data = [element_chimique for element_chimique in data if element_chimique.un == un]

    if libelle_element is not None:
        if not any(element_chimique.libelle_element == libelle_element for element_chimique in data):
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Aucun libellé trouvé")
        data = [element_chimique for element_chimique in data if element_chimique.libelle_element == libelle_element]

    if len(data) == 0:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Aucun élément chimique trouvé")

    if skip >= len(data):
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=f"Skip est plus grand que le nombre d'élément chimique ({len(data)})")

    if limit > len(data):
        limit = len(data)

    if url[-1] != "?":
        url += "&"

    response = {"elements": [element_chimique for element_chimique in data[skip:skip + limit]] }

    if skip + limit < len(data):
        response["nextPage"] = f"{url}skip={str(skip + limit)}&limit={str(limit)}"
    if skip > 0:
        response["previousPage"] = f"{url}skip={str(skip - limit)}&limit={str(limit)}"

    return response


@router.get("/{code_element}", status_code=status.HTTP_200_OK)
def read_element_chimique(code_element: str):
    """
    Récupère une ligne de la table Element_Chimique
    ### Paramètres
    - code_element: Le code de l'élément chimique
    ### Retour
    - un objet de type ElementChimique
    - un message d'erreur en cas d'erreur
    - un status code correspondant
    """

    data = session.query(ElementChimique).filter(ElementChimique.code_element == code_element).first()

    if not data:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Élément chimique introuvable")

    return {"element_chimique": data}