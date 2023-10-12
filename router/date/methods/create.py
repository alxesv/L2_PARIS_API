from database import session
from router.date.date import router
from models import Date
from pydantic import BaseModel
from fastapi import HTTPException
from datetime import datetime as dt

class DateBase(BaseModel):
    date: str

@router.post("/", status_code=201)
def create_date(datetime: DateBase):
    """
   Ajoute une ligne dans la table date
    ### Paramètres
    - date: objet de type Date, avec le champ date
    ### Retour
    - Status code 201 si tout s'est bien passé avec un message de confirmation
    - Message d'erreur avec le status code correspondant sinon
    """
    try:
        # Vérifiez si datetime.date est une chaîne de caractères au format YYYY-MM-DD
        datetime_obj = dt.strptime(datetime.date, "%Y-%m-%d")
    except ValueError:
        raise HTTPException(status_code=400, detail="Format de date invalide. Utilisez le format 'YYYY-MM-DD'.")

    dates = session.query(Date).all()
    for date in dates:
        if date.date == datetime.date:
            raise HTTPException(status_code=400, detail="Date déjà existante")

    try:
        # Ajoutez la date à la base de données
        new_date = Date(date=datetime.date)
        session.add(new_date)
        session.commit()
        return {"message": "Date créée avec succès", "date": new_date.date}

    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
