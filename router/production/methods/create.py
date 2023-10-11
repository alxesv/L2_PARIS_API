from database import session
from router.production.production import router
from models import Production
from pydantic import BaseModel
from fastapi import status, HTTPException


class ProductionBase(BaseModel):
    code_production: int
    un: str
    nom_production: str
@router.post("/", status_code=status.HTTP_201_CREATED)
def create_production(production: ProductionBase):
    """
    Ajoute une ligne dans la table production
    ### Paramètres
    - production : objet de type Production, avec les champs code_production, un et nom_production
    ### Retour
    - Status code 201 si tout s'est bien passé avec message de confirmation
    - Message d'erreur avec le status code correspondant sinon
    """
    productions = session.query(Production).all()

    for code_production in productions:
        if code_production.code_production == production.code_production:
            raise HTTPException(status_code=400, detail="Production déjà existante")
    try:
        production = Production(code_production=production.code_production, un=production.un, nom_production=production.nom_production)
        session.add(production)
        session.commit()
        return {"message": "Production créée avec succès", "production": [{"code_production": production.code_production, "un": production.un, "nom_production": production.nom_production}]}

    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))