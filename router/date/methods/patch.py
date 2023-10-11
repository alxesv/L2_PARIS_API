from database import session
from router.date.date import router
from models import Date
from pydantic import BaseModel

class DateBase(BaseModel):
    date: str

@router.patch("/{datetime}")
def update_date(datetime: str, new_date: DateBase):
    """
    Modifie une ligne dans la table unite
    ### Paramètres
    - unite: le nom de l'unite
    - new_unite: objet de type Unite, avec le champs un
    ### Retour
    - un message de confirmation ou d'erreur
    - un status code correspondant
    """
    dates = session.query(Date).all()
    for date in dates:
        if date.date == datetime:
            date.date = new_date.date
            session.commit()
            return {"message": "Date modifiée avec succès", "status": 200}

    return {"message": "Date non trouvée", "status": 404}