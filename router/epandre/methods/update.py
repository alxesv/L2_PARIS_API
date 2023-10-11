from database import session
from router.epandre.epandre import router
from models import Epandre
from fastapi import HTTPException
from pydantic import BaseModel

class EpandreBase(BaseModel):
    id_engrais: int
    no_parcelle: int
    date: str
    qte_epandue: int = None

@router.patch('/', status_code=200)
def modify_epandre(epandre_id: EpandreBase):
    """
    Modifie une ligne dans la table epandre
    ### Paramètres
    - epandre_id: objet de type Epandre, avec les champs id_engrais, no_parcelle et date
    ### Retour
    - un message de confirmation ou d'erreur
    - un status code correspondant
    """
    pass