from database import session
from router.engrais.engrais import router
from models import Engrais
from models import Unite
from pydantic import BaseModel

class EngraisBase(BaseModel):
    nom_engrais: str = None
    un: str = None
@router.patch("/{id_engrais}")
def modify_engrais(id_engrais: int, updated_engrais: EngraisBase):
    """
    Modifie une ligne dans la table engrais
    ### Paramètres
    - id_engrais: l'identifiant de l'engrais
    - updated_engrais: objet de type Engrais, avec les champs un et nom_engrais
    ### Retour
    - un message de confirmation ou d'erreur
    - un status code correspondant
    """

    if updated_engrais.nom_engrais is None and updated_engrais.un is None:
        return {"message": "Aucun paramètre à modifier", "status": 400}

    all_engrais = session.query(Engrais).all()

    if not any(engrais.id_engrais == id_engrais for engrais in all_engrais):
        return {"message": "Engrais non trouvé", "status": 404}

    if updated_engrais.un is not None:
        all_unites = session.query(Unite).all()
        if not any(unite.un == updated_engrais.un for unite in all_unites):
            return {"message": "Unite non trouvée", "status": 404}
    if updated_engrais.nom_engrais is not None:
        for engrais in all_engrais:
            if engrais.nom_engrais == updated_engrais.nom_engrais and engrais.id_engrais != id_engrais:
                return {"message": "Engrais déjà existant", "status": 400}

    try:
        engrais = session.query(Engrais).filter(Engrais.id_engrais == id_engrais).first()
        if updated_engrais.nom_engrais is not None:
            engrais.nom_engrais = updated_engrais.nom_engrais
        else:
            updated_engrais.nom_engrais = engrais.nom_engrais
        if updated_engrais.un is not None:
            engrais.un = updated_engrais.un
        else:
            updated_engrais.un = engrais.un
        session.commit()
        return {"message": "Engrais modifié avec succès", "status": 200, "engrais": updated_engrais.model_dump()}
    except Exception as e:
        return {"message": str(e), "status": 400}
