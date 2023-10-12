from database import session
from router.element_chimique.element_chimique import router
from models import ElementChimique
from models import Unite
from fastapi import HTTPException, status
from pydantic import BaseModel


class ElementChimiqueBase(BaseModel):
    un: str = None
    libelle_element: str = None


@router.patch("/{code_element}", status_code=status.HTTP_200_OK)
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
    if new_element_chimique.un is None and new_element_chimique.libelle_element is None:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Il manque un paramètre")

    all_elements = session.query(ElementChimique).all()

    if not any(element_chimique.code_element == code_element for element_chimique in all_elements):
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Élément chimique non trouvé")

    if new_element_chimique.un is not None:
        all_unites = session.query(Unite).all()
        if not any(unite.un == new_element_chimique.un for unite in all_unites):
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Unite non trouvée")

    try:
        element_chimique = session.query(ElementChimique).filter(ElementChimique.code_element == code_element).first()
        if new_element_chimique.un is not None:
            element_chimique.un = new_element_chimique.un
        else:
            new_element_chimique.un = element_chimique.un
        if new_element_chimique.libelle_element is not None:
            element_chimique.libelle_element = new_element_chimique.libelle_element
        else:
            new_element_chimique.libelle_element = element_chimique.libelle_element
        session.commit()
        return {"message": "Élément chimique modifié avec succès", "element": new_element_chimique.model_dump()}
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))
