from database import session
from router.posseder.posseder import router
from models import Posseder
from fastapi import HTTPException, status
from pydantic import BaseModel

class PossederBase(BaseModel):
    id_engrais: int
    code_element: str
    valeur: int

@router.patch('/', status_code=status.HTTP_200_OK)
def modify_posseder(posseder_id: PossederBase):
    """
    Modifie une ligne dans la table posseder
    ### Paramètres
    - posseder_id: objet de type Posseder, avec les champs id_posseder, code_element et valeur
    ### Retour
    - un message de confirmation ou d'erreur
    - un status code correspondant
    """
    pass