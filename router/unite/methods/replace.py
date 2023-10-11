from database import session
from router.unite.unite import router
from models import Unite
from pydantic import BaseModel

class UniteBase(BaseModel):
    un: str

@router.put("/{unite}")
def replace_unite(unite: str, new_unite: UniteBase):
    """
    Remplace une ligne dans la table unite
    ### Paramètres
    - unite: le nom de l'unite
    - new_unite: objet de type Unite, avec le champs un
    ### Retour
    - un message de confirmation ou d'erreur
    - un status code correspondant
    """
    unites = session.query(Unite).all()

    if len(new_unite.un) == 0:
        return {"message": "Unite vide", "status": 400}

    if new_unite.un in [un.un for un in unites]:
        return {"message": "Unite déjà existante", "status": 400}

    for un in unites:
        if un.un == unite:
            un.un = new_unite.un
            session.commit()
            return {"message": "Unite remplacée avec succès", "status": 200}

    return {"message": "Unite non trouvée", "status": 404}