from database import session
from router.unite.unite import router
from models import Unite
from fastapi import HTTPException

@router.delete("/{unite}", status_code=200)
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
            return {"message": "Unite supprimée avec succès"}

    raise HTTPException(status_code=404, detail="Unite non trouvée")
