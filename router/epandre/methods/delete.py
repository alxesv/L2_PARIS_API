from database import session
from router.epandre.epandre import router
from models import Epandre
from fastapi import HTTPException
from pydantic import BaseModel
from models import Date

class EpandrePrimary(BaseModel):
    id_engrais: int
    no_parcelle: int
    date: str
@router.delete("/", status_code=200)
def delete_epandre(epandre_id: EpandrePrimary):
    """
    Supprime une ligne dans la table epandre
    ### Paramètres
    - epandre_id: objet de type EpandrePrimary, avec les champs id_engrais, no_parcelle et date
    ### Retour
    - un message de confirmation ou d'erreur
    - un status code correspondant
    """
    if epandre_id.id_engrais is None or epandre_id.no_parcelle is None or epandre_id.date is None:
        raise HTTPException(status_code=400, detail="Il manque au moins un paramètre")

    dates = session.query(Date).all()
    if not any(date.date == epandre_id.date for date in dates):
        raise HTTPException(status_code=404, detail="Date non trouvée")
    else:
        date_object = session.query(Date).filter(Date.date == epandre_id.date).first()

    epandres = session.query(Epandre).all()
    for epandre in epandres:
        if epandre.id_engrais == epandre_id.id_engrais and epandre.no_parcelle == epandre_id.no_parcelle and epandre.date == date_object:
            deleted_epandre = epandre_id.model_dump()
            session.delete(epandre)
            session.commit()
            return {"message": "Epandre supprimé avec succès", "deleted_epandre": deleted_epandre}
    raise HTTPException(status_code=404, detail="Epandre non trouvé")
