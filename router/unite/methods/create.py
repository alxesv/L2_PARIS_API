from database import session
from router.unite.unite import router
from models import Unite
from pydantic import BaseModel
from fastapi import HTTPException

class UniteBase(BaseModel):
    un: str
@router.post("/", status_code=201)
def create_unite(unite: UniteBase):
    """
   Ajoute une ligne dans la table unite
    ### Paramètres
    - unite: objet de type Unite, avec le champs un
    ### Retour
    - Status code 201 si tout s'est bien passé avec message de confirmation
    - Message d'erreur avec le status code correspondant sinon
    """

    unites = session.query(Unite).all()
    for un in unites:
        if un.un == unite.un:
            raise HTTPException(status_code=400, detail="Unite déjà existante")


    try:
        unite = Unite(un=unite.un)
        session.add(unite)
        session.commit()
        return {"message": "Unite créée avec succès", "unite": unite.un}

    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
