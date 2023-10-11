from database import session
from router.unite.unite import router
from models import Unite

@router.delete("/{unite}")
def delete_unite(unite: str):
    """
    Supprime une ligne dans la table unite
    ### Paramètres
    - unite: le nom de l'unite
    ### Retour
    - un message de confirmation ou d'erreur
    - un status code correspondant
    """
    unites = session.query(Unite).all()
    for un in unites:
        if un.un == unite:
            session.delete(un)
            session.commit()
            return {"message": "Unite supprimée avec succès", "status": 200}

    return {"message": "Unite non trouvée", "status": 404}