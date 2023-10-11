from database import session
from router.engrais.engrais import router
from models import Engrais
from models import Unite
from pydantic import BaseModel
class EngraisBase(BaseModel):
    un: str
    nom_engrais: str
@router.put("/{id_engrais}")
def replace_engrais(id_engrais: int, new_engrais: EngraisBase):
    """
    Remplace une ligne dans la table engrais
    ### Paramètres
    - id_engrais: l'identifiant de l'engrais
    - new_engrais: objet de type Engrais, avec les champs un et nom_engrais
    ### Retour
    - un message de confirmation ou d'erreur
    - un status code correspondant
    """
    if new_engrais.nom_engrais is None or new_engrais.un is None:
        return {"message": "Il manque un paramètre", "status": 400}

    all_engrais = session.query(Engrais).all()

    if not any(engrais.id_engrais == id_engrais for engrais in all_engrais):
        return {"message": "Engrais non trouvé", "status": 404}

    if new_engrais.un is not None:
        all_unites = session.query(Unite).all()
        if not any(unite.un == new_engrais.un for unite in all_unites):
            return {"message": "Unite non trouvée", "status": 404}
    if new_engrais.nom_engrais is not None:
        for engrais in all_engrais:
            if engrais.nom_engrais == new_engrais.nom_engrais and engrais.id_engrais != id_engrais:
                return {"message": "Engrais déjà existant", "status": 400}

    try:
        engrais = session.query(Engrais).filter(Engrais.id_engrais == id_engrais).first()
        for (key, value) in new_engrais:
            setattr(engrais, key, value)
        session.commit()
        return {"message": "Engrais modifié avec succès", "status": 200, "engrais": new_engrais.model_dump()}
    except Exception as e:
        return {"message": str(e), "status": 400}
