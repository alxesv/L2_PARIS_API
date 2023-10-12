from database import session
from router.posseder.posseder import router
from models import Posseder, Engrais, ElementChimique
from fastapi import HTTPException, status
from pydantic import BaseModel

class PossederBase(BaseModel):
    id_engrais: int
    code_element: str
    valeur: int

@router.post("/", status_code=status.HTTP_201_CREATED)
def create_posseder(posseder: PossederBase):
    """
    Ajoute une ligne dans la table posseder
    ### Paramètres
    - posseder: objet de type Posseder, avec les champs id_engrais, code_element et valeur
    ### Retour
    - Status code 201 si tout s'est bien passé avec message de confirmation
    - Message d'erreur avec le status code correspondant sinon
    """
    posseders = session.query(Posseder).all()

    code_elements = session.query(ElementChimique).all()
    if not any(code_element.code_element == posseder.code_element for code_element in code_elements):
        raise HTTPException(status_code=404, detail="Code de l'élément non trouvé")

    engrais = session.query(Engrais).all()
    if not any(engrais_item.id_engrais == posseder.id_engrais for engrais_item in engrais):
        raise HTTPException(status_code=404, detail="Engrais non trouvé")

    for posseder_item in posseders:
        if posseder_item.id_engrais == posseder.id_engrais and posseder_item.code_element == posseder.code_element:
            raise HTTPException(status_code=400, detail="Possession déjà existante")

    try:
        add_posseder = Posseder(id_engrais=posseder.id_engrais, code_element=posseder.code_element, valeur=posseder.valeur)
        session.add(add_posseder)
        session.commit()
        return {"message": "Possession créée avec succès", "posseder": posseder.model_dump()}

    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
