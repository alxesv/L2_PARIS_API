from database import session
from router.production.production import router
from models import Production
from fastapi import status, HTTPException

@router.delete("/{production}", status_code=status.HTTP_200_OK)
def delete_production(production: int):
    """
    Supprime une ligne dans la table production
    ### Paramètres
    - production : le code_production de la production
    ### Retour
    - Status code 200 si tout s'est bien passé avec message de confirmation
    - Message d'erreur avec le status code correspondant sinon
    """
    productions = session.query(Production).all()
    for code_production in productions:
        if code_production.code_production == production:
            session.delete(code_production)
            session.commit()
            return {"message": "Production supprimée avec succès"}

    raise HTTPException(status_code=404, detail="La production n'a pas été trouvée")