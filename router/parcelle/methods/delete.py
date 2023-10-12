from database import session
from router.parcelle.parcelle import router
from models import Parcelle
from fastapi import HTTPException

@router.delete("/{parcelle}",status_code=201)
def delete_parcelle(parcelle: int):
    """
    Supprime une ligne dans la table parcelle
    ### Paramètres
    - parcelle: l'id de la table Parcelle utilisé pour trouver l'élément cherché à supprimer
    ### Retour
    - un message de confirmation ou d'erreur
    - un status code correspondant
    """
    parcelles = session.query(Parcelle).all()
    for no_parcelle in parcelles:
        if no_parcelle.no_parcelle == parcelle:
            session.delete(no_parcelle)
            session.commit()
            return {"message": "Parcelle supprimée avec succès"}
    raise HTTPException(status_code=404,detail="Parcelle non trouvée")