from database import session
from router.posseder.posseder import router
from models import Posseder
from fastapi import HTTPException, status

@router.delete("/", status_code=status.HTTP_200_OK)
def delete_posseder(id_engrais: int = None, code_element: str = None):
    """
    Supprime une ligne dans la table posseder
    ### Paramètres
    - posseder_id: objet de type PossederPrimary, avec les champs id_engrais et code_element
    ### Retour
    - un message de confirmation ou d'erreur
    - un status code correspondant
    """
    if id_engrais is None or code_element is None:
        raise HTTPException(status_code=400, detail="Il manque au moins un paramètre")

    posseders = session.query(Posseder).all()
    for posseder in posseders:
        if posseder.id_engrais == id_engrais and posseder.code_element == code_element:
            deleted_posseder = posseder
            session.delete(posseder)
            session.commit()
            return {"message": "Possession supprimée avec succès", "deleted_posseder ": deleted_posseder}
    raise HTTPException(status_code=404, detail="Possession non trouvée")