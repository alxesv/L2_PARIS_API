from database import session
from router.epandre.epandre import router
from models import Epandre
from fastapi import HTTPException
from models import Date

@router.delete("/", status_code=200)
def delete_epandre(id_engrais: int, no_parcelle: int, date: str):
    """
    Supprime une ligne dans la table epandre
    ### Paramètres
    - epandre_id: objet de type EpandrePrimary, avec les champs id_engrais, no_parcelle et date
    ### Retour
    - un message de confirmation ou d'erreur
    - un status code correspondant
    """

    dates = session.query(Date).all()
    if not any(orm_date.date == date for orm_date in dates):
        raise HTTPException(status_code=404, detail="Date non trouvée")
    else:
        date_object = session.query(Date).filter(Date.date == date).first()

    epandres = session.query(Epandre).all()
    for epandre in epandres:
        if epandre.id_engrais == id_engrais and epandre.no_parcelle == no_parcelle and epandre.date == date_object:
            deleted_epandre = epandre
            session.delete(epandre)
            session.commit()
            return {"message": "Epandre supprimé avec succès", "deleted_epandre": deleted_epandre}
    raise HTTPException(status_code=404, detail="Epandre non trouvé")
