from database import session
from router.production.production import router
from models import Production, Unite
from pydantic import BaseModel
from fastapi import HTTPException, status

class ProductionBase(BaseModel):
    un: str
    nom_production: str
@router.put("/{code_production}", status_code=status.HTTP_200_OK)
def replace_production(code_production: int, new_production: ProductionBase):
    """
    Remplace une ligne dans la table production
    ### Paramètres
    - code_production: le code de la production
    - new_production: objet de type Production, avec les champs un et nom_production
    ### Retour
    - un message de confirmation ou d'erreur
    - un status code correspondant
    """
    all_productions = session.query(Production).all()

    if not any(production.code_production == code_production for production in all_productions):
        raise HTTPException(status_code=404, detail="Production non trouvée")

    if new_production.un is not None:
        all_unites = session.query(Unite).all()
        if not any(unite.un == new_production.un for unite in all_unites):
            raise HTTPException(status_code=404, detail="Unite non trouvée")
    if new_production.nom_production is not None:
        for production in all_productions:
            if production.nom_production == new_production.nom_production and production.code_production != code_production:
                raise HTTPException(status_code=400, detail="Production déjà existante")

    try:
        production = session.query(Production).filter(Production.code_production == code_production).first()
        for (key, value) in new_production:
            setattr(production, key, value)
        session.commit()
        return {"message": "Production modifiée avec succès", "production": new_production.model_dump()}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))