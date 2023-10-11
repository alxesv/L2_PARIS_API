from database import session
from router.engrais.engrais import router
from models import Engrais
from models import Unite


@router.get("/")
def read_engrais(skip: int = 0, limit: int = 10, sort: str = None, un: str = None):
    """
    Récupère les lignes de la table engrais
    ### Paramètres
    - skip: nombre d'éléments à sauter
    - limit: nombre d'éléments à retourner
    - sort: le ou les champs sur lequel trier les résultats
    - un: le nom de l'unite a filtrer
    ### Retour
    - un tableau d'objets de type Engrais
    - un message d'erreur en cas d'erreur
    - un status code correspondant
    - url de navigation pour la pagination
    """
    url = f"http://127.0.0.1:8000/engrais?"

    data = session.query(Engrais).all()

    sortable = Engrais.__table__.columns.keys()

    if sort is not None:
        sort_url = ""
        sort = sort.split(",")
        for s in sort:
            if s[0] == "-":
                check_sort = s[1:]
            else:
                check_sort = s
            if check_sort not in sortable:
                return {"message": f"Le champ de tri {check_sort} n'existe pas", "status": 400}
            if s[0] == "-":
                data = session.query(Engrais).order_by(getattr(Engrais, s[1:]).desc()).all()
                sort_url += f"-{s[1:]},"
            else:
                data = session.query(Engrais).order_by(getattr(Engrais, s)).all()
                sort_url += f"{s},"
        if url[-1] != "?":
            url += "&"
        url += f"sort={sort_url[:-1]}"


    if un is not None:
        if not any(engrais.un == un for engrais in data):
            return {"message": "Unite non trouvée", "status": 404}
        data = [engrais for engrais in data if engrais.un == un]

    if len(data) == 0:
        return {"message": "Aucune unite trouvée", "status": 404}

    if skip >= len(data):
        return {"message": "Skip est plus grand que le nombre d'unite", "status": 400}

    if limit > len(data):
        limit = len(data)

    if url[-1] != "?":
        url += "&"

    response = {"status": 200, "engrais": data[skip:skip + limit]}

    if skip + limit < len(data):
        response["nextPage"] = f"{url}skip={str(skip + limit)}&limit={str(limit)}"
    if skip > 0:
        response["previousPage"] = f"{url}skip={str(skip - limit)}&limit={str(limit)}"

    return response

@router.get("/{id_engrais}")
def read_engrais_by_id(id_engrais: int):
    """
    Récupère une ligne dans la table engrais
    ### Paramètres
    - id_engrais: l'identifiant de l'engrais
    ### Retour
    - un message de confirmation ou d'erreur
    - un object de type Engrais
    - un status code correspondant
    """
    data = session.query(Engrais).filter(Engrais.id_engrais == id_engrais).first()

    if not data:
        return {"message": "Engrais introuvable", "status": 404}

    return {"status": 200, "engrais": data}
