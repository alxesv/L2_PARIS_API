from database import session
from router.date.date import router
from models import Date
from fastapi import HTTPException
@router.delete("/{datetime}",status_code=200)
def delete_date(datetime:str):
    """
        Supprime une ligne dans la table date
        ### Paramètres
        - date: la string de la date selectionner
        ### Retour
        - un message de confirmation ou d'erreur
        - un status code correspondant
    """

    dates=session.query(Date).all()
    for date in dates:
        if date.date==datetime:
            session.delete(date)
            session.commit()
            return {"message": "Date supprimée avec succès"}
    raise HTTPException(status_code=404,detail="Date non trouvée")