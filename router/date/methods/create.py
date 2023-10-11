from database import session
from router.date.date import router
from models import Date
from pydantic import BaseModel


class DateBase(BaseModel):
    date: str
@router.post("/")
def create_date(datetime: DateBase):
    """
   Ajoute une ligne dans la table date
    ### Paramètres
    - date: objet de type Date, avec le champs date
    ### Retour
    - Status code 201 si tout s'est bien passé avec message de confirmation
    - Message d'erreur avec le status code correspondant sinon
    """

    dates = session.query(Date).all()
    for date in dates:
        if date.date == datetime.date:
            return {"message": "Date déjà existante", "status": 400}

    try:
        datetime = Date(date=datetime.date)
        session.add(datetime)
        session.commit()
        return {"message": "Date créée avec succès", "status": 201, "date": datetime.date}
    except Exception as e:
        return {"message": str(e), "status": 400}