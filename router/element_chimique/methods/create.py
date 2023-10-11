from database import session
from router.element_chimique.element_chimique import router
from models import ElementChimique
from pydantic import BaseModel


class ElementChimiqueBase(BaseModel):
    code_element: str
    un: str
    libelle_element: str


@router.post("/")
def create_element_chimique(new_element_chimique: ElementChimiqueBase):
    """
   Ajoute une ligne dans la table unite
    ### Paramètres
    - code_element : Code de l'élément chimique
    - un : Nom de l'unité
    - libelle_element : Description de l'élément
    ### Retour
    - Status code 201 si tout s'est bien passé avec message de confirmation
    - Message d'erreur avec le status code correspondant sinon
    """

    element_chimiques = session.query(ElementChimique).all()
    for elt_chimique in element_chimiques:
        if elt_chimique.code_element == new_element_chimique.code_element:
            return {"message": "Élément déjà existant", "status": 400}

    try:
        element_chimique = ElementChimique(code_element=new_element_chimique.code_element,
                                           un=new_element_chimique.un, libelle_element=new_element_chimique.libelle_element)
        session.add(element_chimique)
        session.commit()
        return {"message": "Élément créé avec succès", "status": 201, "element": new_element_chimique}

    except Exception as e:
        return {"message": str(e), "status": 400}
