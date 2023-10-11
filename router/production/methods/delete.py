from database import session
from router.production.production import router
from models import Production

@router.delete("/{production}")
def delete_production(production: int):
    """
    Supprime une ligne dans la table production
    ### Paramètres
    - production : l'id de la production
    ### Retour
    - Status code 200 si tout s'est bien passé avec message de confirmation
    - Message d'erreur avec le status code correspondant sinon
    """
    productions = session.query(Production).all()
    for code_production in productions:
        if code_production.code_production == production:
            session.delete(code_production)
            session.commit()
            return {"message": "Unite supprimée avec succès", "status": 200}

    return {"message": "Unite non trouvée", "status": 404}