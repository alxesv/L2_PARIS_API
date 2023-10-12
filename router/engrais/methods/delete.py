from database import session
from router.engrais.engrais import router
from models import Engrais
from fastapi import HTTPException
@router.delete("/{id_engrais}", status_code=200)
def delete_engrais(id_engrais: int):
    """
    Supprime une ligne dans la table engrais
    ### Paramètres
    - id_engrais: l'identifiant de l'engrais
    ### Retour
    - un message de confirmation ou d'erreur
    - un status code correspondant
    """
    engrais = session.query(Engrais).all()
    for engrais_item in engrais:
        if engrais_item.id_engrais == id_engrais:
            deleted_engrais_name = engrais_item.nom_engrais
            session.delete(engrais_item)
            session.commit()
            return {"message": "Engrais supprimé avec succès", "deleted_engrais": deleted_engrais_name}
    raise HTTPException(status_code=404, detail="Engrais non trouvé")
