from database import session
from router.production.production import router
from models import Production
from pydantic import BaseModel


class ProductionBase(BaseModel):
    code_production: int
    un: str
    nom_production: str
@router.post("/")
def create_production(production: ProductionBase):
    """
    Ajoute une ligne dans la table production
    ### Paramètres
    - production : objet de type Production, avec les champs code_production, un et nom_production
    ### Retour
    - Status code 201 si tout s'est bien passé avec message de confirmation
    - Message d'erreur avec le status code correspondant sinon
    """
    try:
        productions = session.query(Production).all()
        for code_production, un, nom_production in productions:
            print(code_production, un, nom_production)
        if production in productions:
            raise Exception("Unite déjà existante")

        return {"message": "Unite créée avec succès", "status": 201, "production": productions}

    except Exception as e:
        return {"message": str(e), "status": 400}
