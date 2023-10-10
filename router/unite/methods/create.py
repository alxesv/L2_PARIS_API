from database import session
from router.unite.unite import router
from models import Unite
from pydantic import BaseModel


class UniteBase(BaseModel):
    un: str
@router.post("/")
def create_unite(unite: UniteBase):
    """
   Ajoute une ligne dans la table unite
    ### Paramètres
    - unite: objet de type Unite, avec le champs un
    ### Retour
    - Status code 201 si tout s'est bien passé avec message de confirmation
    - Message d'erreur avec le status code correspondant sinon
    """
    try:
        unites = session.query(Unite).all()
        for un in unites:
            print(un)
        if unite in unites:
            raise Exception("Unite déjà existante")

        return {"message": "Unite créée avec succès", "status": 201, "unite": unite}

    except Exception as e:
        return {"message": str(e), "status": 400}
