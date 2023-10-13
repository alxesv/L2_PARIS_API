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
    for parcelle_item in parcelles:
        if parcelle_item.no_parcelle == parcelle:
            deleted_parcelle = parcelle_item
            session.delete(parcelle_item)
            session.commit()
            return {"message": "Parcelle supprimée avec succès", "deleted_parcelle": deleted_parcelle}
    raise HTTPException(status_code=404,detail="Parcelle non trouvée")