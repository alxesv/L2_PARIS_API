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
    """


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
