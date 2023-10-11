from database import session
from router.date.date import router
from models import Date

@router.delete("/{date}")
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
            return {"message": "Date supprimée avec succès", "status": 200}
    return {"message": "Date non trouvée", "status": 404}