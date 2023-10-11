from database import session
from router.epandre.epandre import router
from models import Epandre
from fastapi import HTTPException
from pydantic import BaseModel
from models import Date

class EpandreBase(BaseModel):
    id_engrais: int
    no_parcelle: int
    date: str
    qte_epandue: int

@router.put('/', status_code=200)
def replace_epandre(new_epandre: EpandreBase):
    """
    Remplace une ligne dans la table epandre
    ### Paramètres
    - epandre: objet de type Epandre, avec les champs id_engrais, no_parcelle et date
    ### Retour
    - un message de confirmation ou d'erreur
    - un status code correspondant
    """
    if new_epandre.id_engrais is None or new_epandre.no_parcelle is None or new_epandre.date is None or new_epandre.qte_epandue is None:
        raise HTTPException(status_code=400, detail="Il manque au moins un paramètre")

    dates = session.query(Date).all()
    if not any(date.date == new_epandre.date for date in dates):
        raise HTTPException(status_code=404, detail="Date non trouvée")
    else:
        date_object = session.query(Date).filter(Date.date == new_epandre.date).first()

    epandres = session.query(Epandre).all()
    for epandre in epandres:
        if epandre.id_engrais == new_epandre.id_engrais and epandre.no_parcelle == new_epandre.no_parcelle and epandre.date == date_object:
            epandre.qte_epandue = new_epandre.qte_epandue
            new_epandre = new_epandre.model_dump()
            session.commit()
            return {"message": "Epandre remplacée avec succès", "new_epandre": new_epandre}
    raise HTTPException(status_code=404, detail="Epandre non trouvé")