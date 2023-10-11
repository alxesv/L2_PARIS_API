from database import session
from router.element_chimique.element_chimique import router
from models import ElementChimique
from fastapi import HTTPException, status


@router.delete("/{code_element}", status_code=status.HTTP_200_OK)
def delete_element_chimique(code_element: str):
    """
    Supprime une ligne dans la table engrais
    ### Paramètres
    - id_engrais: l'identifiant de l'engrais
    ### Retour
    - un message de confirmation ou d'erreur
    - un status code correspondant
    """
    element_chimiques = session.query(ElementChimique).all()
    for element_chimique in element_chimiques:
        if element_chimique.code_element == code_element:
            deleted_engrais_name = element_chimique.code_element
            session.delete(element_chimique)
            session.commit()
            return {"message": "Élément chimique supprimé avec succès", "deleted_element": deleted_engrais_name}
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Élément chimique non trouvé")
