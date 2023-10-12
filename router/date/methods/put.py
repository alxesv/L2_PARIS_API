from database import session
from router.date.date import (router)
from models import Date
from pydantic import BaseModel
from fastapi import HTTPException
from datetime import datetime as dt


class DateBase(BaseModel):
    date: str

@router.put("/{datetime}",status_code=200)
def update_date(datetime: str, new_date: DateBase):
    """
    Remplace une ligne dans la table date
    ### Paramètres
    - date: la date
    - new_date: objet de type Date, avec le champs date
    ### Retour
    - un message de confirmation ou d'erreur
    - un status code correspondant
    """
    try:
        # Vérifiez si datetime.date est une chaîne de caractères au format YYYY-MM-DD
        datetime_obj = dt.strptime(datetime.date, "%Y-%m-%d")
    except ValueError:
        raise HTTPException(status_code=400, detail="Format de date invalide. Utilisez le format 'YYYY-MM-DD'.")

    dates = session.query(Date).all()
    for date in dates:
        if date.date == datetime:
            date.date = new_date.date
            session.commit()
            return {"message": "Date remplacée avec succès"}
    raise HTTPException(status_code=404, detail="Date non trouvée")
