from database import session
from router.date.date import router
from models import Date
from pydantic import BaseModel
from fastapi import HTTPException
from datetime import datetime as dt

class DateBase(BaseModel):
    date: str

@router.patch("/{date}", status_code=200)
def replace_date(date: str, new_date: DateBase):
    """
    Modifie une ligne dans la table date
    ### Paramètres
    - date: le nom de la date à modifier
    - new_date: objet de type DateBase, avec le champ date
    ### Retour
    - un message de confirmation ou d'erreur
    - un status code correspondant
    """
    try:
        # Vérifiez si date est une chaîne de caractères au format YYYY-MM-DD
        datetime_obj = dt.strptime(date, "%Y-%m-%d")
    except ValueError:
        raise HTTPException(status_code=400, detail="Format de date invalide. Veuillez respecter ce format -> %Y-%m-%d")

    existing_date = session.query(Date).filter(Date.date == date).first()
    if existing_date:
        try:
            # Mettez à jour la date existante dans la base de données
            existing_date.date = new_date.date
            session.commit()
            return {"message": "Date modifiée avec succès"}
        except Exception as e:
            raise HTTPException(status_code=500, detail=str(e))
    else:
        raise HTTPException(status_code=404, detail="Date non trouvée")
