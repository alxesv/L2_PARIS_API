from database import session
from router.unite.unite import router
from models import Unite
from pydantic import BaseModel

class UniteBase(BaseModel):
    un: str

@router.patch("/{unite}")
def update_unite(unite: str, new_unite: UniteBase):
    """
    Modifie une ligne dans la table unite
    ### Paramètres
    - unite: le nom de l'unite
    - new_unite: objet de type Unite, avec le champs un
    ### Retour
    - un message de confirmation ou d'erreur
    - un status code correspondant
    """
    unites = session.query(Unite).all()
    for un in unites:
        if un.un == unite:
            un.un = new_unite.un
            session.commit()
            return {"message": "Unite modifiée avec succès", "status": 200}

    return {"message": "Unite non trouvée", "status": 404}