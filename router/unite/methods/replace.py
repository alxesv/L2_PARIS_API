from database import session
from router.unite.unite import router
from models import Unite
from pydantic import BaseModel
from fastapi import HTTPException

class UniteBase(BaseModel):
    un: str

@router.put("/{unite}", status_code=200)
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
        raise HTTPException(status_code=400, detail="Unite vide")

    if new_unite.un in [un.un for un in unites]:
        raise HTTPException(status_code=400, detail="Unite déjà existante")

    for un in unites:
        if un.un == unite:
            un.un = new_unite.un
            session.commit()
            return {"message": "Unite remplacée avec succès"}

    raise HTTPException(status_code=404, detail="Unite non trouvée")
