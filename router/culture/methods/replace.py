from database import session
from router.culture.culture import router
from models import Culture, Parcelle, Production
from pydantic import BaseModel
from fastapi import HTTPException, status


class CultureBase(BaseModel):
    no_parcelle: int
    code_production: int
    date_debut: str
    date_fin: str
    qte_recoltee: int


@router.put("/{identifiant_culture}", status_code=status.HTTP_200_OK)
def replace_culture(identifiant_culture: int, new_culture: CultureBase):
    """
    Remplace une ligne dans la table Culture
    ### Paramètres
    - identifiant_culture: Identifiant de la culture à remplacé
    - new_culture: objet de type Culture, avec les champs relatifs à Culture
    ### Retour
    - un message de confirmation ou d'erreur
    - un status code correspondant
    """
    all_culture = session.query(Culture).all()

    if not any(culture.identifiant_culture == identifiant_culture for culture in all_culture):
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Culture non trouvée")

    if new_culture.no_parcelle is not None:
        all_parcelles = session.query(Parcelle).all()
        if not any(parcelle.no_parcelle == new_culture.no_parcelle for parcelle in all_parcelles):
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Parcelle non trouvée")

    if new_culture.code_production is not None:
        all_productions = session.query(Production).all()
        if not any(production.code_production == new_culture.code_production for production in all_productions):
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Production non trouvée")

    try:
        culture = session.query(Culture).filter(Culture.identifiant_culture == identifiant_culture).first()
        for (key, value) in new_culture:
            setattr(culture, key, value)
        session.commit()
        return {"message": "Culture modifiée avec succès", "culture": new_culture.model_dump()}
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))