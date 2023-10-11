from database import session
from router.culture.culture import router
from models import Parcelle, Production, Culture
from fastapi import HTTPException, status
from pydantic import BaseModel


class CultureBase(BaseModel):
    no_parcelle: int
    code_production: int
    date_debut: str
    date_fin: str
    qte_recoltee: int


@router.post("/", status_code=status.HTTP_201_CREATED)
def create_culture(new_culture: CultureBase):
    """
   Ajoute une ligne dans la table unite
    ### Paramètres
    - no_parcelle : Numéro de la parcelle attribué à cette culture
    - code_production : Code de la production attribué à cette culture
    - date_debut : Date du début de la culture
    - date_fin : Date de la fin de la culture
    - qte_recoltee : Quantitée récolté provenant de la culture
    ### Retour
    - Status code 201 si tout s'est bien passé avec message de confirmation
    - Message d'erreur avec le status code correspondant sinon
    """

    cultures = session.query(Culture).all()
    for culture in cultures:
        if culture.identifiant_culture == culture.identifiant_culture:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Culture déjà existante")

    parcelles = session.query(Parcelle).all()
    if not any(parcelle.no_parcelle == new_culture.no_parcelle for parcelle in parcelles):
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Numéro de parcelle non trouvée")

    productions = session.query(Production).all()
    if not any(production.code_production == new_culture.code_production for production in productions):
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Code de production non trouvée")

    try:
        culture = Culture(**new_culture.__dict__)
        session.add(culture)
        session.commit()
        return {"message": "Culture créé avec succès", "element": new_culture}

    except Exception as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))
