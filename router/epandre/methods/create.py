from database import session
from router.epandre.epandre import router
from models import Epandre
from fastapi import HTTPException
from models import Engrais
from models import Parcelle
from models import Date
from pydantic import BaseModel

class EpandreBase(BaseModel):
    id_engrais: int
    no_parcelle: int
    date: str
    qte_epandue: int

@router.post("/", status_code=201)
def create_epandre(epandre: EpandreBase):
    """
    Ajoute une ligne dans la table epandre
    ### Paramètres
    - epandre: objet de type Epandre, avec les champs id_engrais, no_parcelle, date_id et qte_epandue
    ### Retour
    - Status code 201 si tout s'est bien passé avec message de confirmation
    - Message d'erreur avec le status code correspondant sinon
    """

    epandres = session.query(Epandre).all()

    dates = session.query(Date).all()
    if not any(date.date == epandre.date for date in dates):
        raise HTTPException(status_code=404, detail="Date non trouvée")

    engrais = session.query(Engrais).all()
    if not any(engrais_item.id_engrais == epandre.id_engrais for engrais_item in engrais):
        raise HTTPException(status_code=404, detail="Engrais non trouvé")

    parcelles = session.query(Parcelle).all()
    if not any(parcelle.no_parcelle == epandre.no_parcelle for parcelle in parcelles):
        raise HTTPException(status_code=404, detail="Parcelle non trouvée")

    date_object = session.query(Date).filter(Date.date == epandre.date).first()

    for epandre_item in epandres:
        if epandre_item.id_engrais == epandre.id_engrais and epandre_item.no_parcelle == epandre.no_parcelle and epandre_item.date == date_object:
            raise HTTPException(status_code=400, detail="Epandre déjà existant")

    try:
        add_epandre = Epandre(id_engrais=epandre.id_engrais, no_parcelle=epandre.no_parcelle, date=date_object, qte_epandue=epandre.qte_epandue)
        session.add(add_epandre)
        session.commit()
        return {"message": "Epandre créé avec succès", "epandre": epandre.model_dump()}

    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
