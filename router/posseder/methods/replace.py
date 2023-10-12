from database import session
from router.posseder.posseder import router
from models import Posseder
from fastapi import HTTPException, status
from pydantic import BaseModel
class PossederBase(BaseModel):
    id_engrais: int
    code_element: str
    valeur: int

@router.put('/', status_code=status.HTTP_201_CREATED)
def replace_posseder(new_posseder: PossederBase):
    """
    Remplace une ligne dans la table posseder
    ### Paramètres
    - posseder: objet de type Posseder, avec les champs id_engrais, code_element et valeur
    ### Retour
    - un message de confirmation ou d'erreur
    - un status code correspondant
    """
    if new_posseder.id_engrais is None or new_posseder.code_element is None:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Il manque au moins un paramètre")

    posseders = session.query(Posseder).all()
    for posseder in posseders:
        if posseder.id_engrais == new_posseder.id_engrais and posseder.code_element == new_posseder.code_element:
            new_posseder = new_posseder.model_dump()
            session.commit()
            return {"message": "Possession remplacée avec succès", "new_posseder": new_posseder}
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Possession non trouvée")