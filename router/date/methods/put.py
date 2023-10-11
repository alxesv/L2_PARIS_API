
from database import session
from router.date.date import (router)
from models import Date
from pydantic import BaseModel

class DateBase(BaseModel):
    date: str

@router.put("/{datetime}")
def replace_date(datetime: str, new_date: DateBase):
    """
    Remplace une ligne dans la table date
    ### Paramètres
    - date: la date
    - new_date: objet de type Date, avec le champs date
    ### Retour
    - un message de confirmation ou d'erreur
    - un status code correspondant
    """
    dates = session.query(Date).all()
    for date in dates:
        if date.date == datetime:
            date.date = new_date.date
            session.commit()
            return {"message": "Date remplacée avec succès", "status": 200}

    return {"message": "Date non trouvée", "status": 404}