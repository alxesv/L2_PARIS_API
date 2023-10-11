from database import session
from router.element_chimique.element_chimique import router
from models import ElementChimique
from models import Unite
from fastapi import HTTPException, status
from .base_model import ElementChimiqueBase


@router.put("/{code_element}", status_code=status.HTTP_200_OK)
def replace_element_chimique(code_element: str, new_element_chimique: ElementChimiqueBase):
    """
    Remplace une ligne dans la table engrais
    ### Paramètres
    - id_engrais: l'identifiant de l'engrais
    - new_engrais: objet de type Engrais, avec les champs un et nom_engrais
    ### Retour
    - un message de confirmation ou d'erreur
    - un status code correspondant
    """
    if new_element_chimique.un is None or new_element_chimique.libelle_element is None:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Il manque un paramètre")

    all_elements = session.query(ElementChimique).all()

    if not any(element_chimique.code_element == code_element for element_chimique in all_elements):
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Élément chimique non trouvé")

    if new_element_chimique.un is not None:
        all_unites = session.query(Unite).all()
        if not any(unite.un == new_element_chimique.un for unite in all_unites):
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Unite non trouvée")

    if new_element_chimique.code_element is not None:
        for element_chimique in all_elements:
            if element_chimique.code_element == new_element_chimique.code_element:
                raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Élément déjà existant")

    try:
        engrais = session.query(ElementChimique).filter(ElementChimique.code_element == code_element).first()
        for (key, value) in new_element_chimique:
            setattr(engrais, key, value)
        session.commit()
        return {"message": "Élément chimique modifié avec succès", "engrais": new_element_chimique.model_dump()}
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))
