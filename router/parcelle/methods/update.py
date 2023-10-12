from database import session
from router.parcelle.parcelle import router
from models import Parcelle
from pydantic import BaseModel
from fastapi import HTTPException

class ParcelleBase(BaseModel):
    surface: int=None
    nom_parcelle: str=None
    coordonnees: str=None


@router.patch("/{no_parcelle}", status_code=200)
def modify_parcelle(no_parcelle: int, updated_parcelle: ParcelleBase):
    """
    Modifie une ligne dans la table parcelle
    ### Paramètres
    - no_parcelle: l'identifiant de parcelle
    - updated_parcelle objet de type Parcelle, avec les champs no_parcelle, nom_parcelle, surface et coordonnees
    ### Retour
    - un message de confirmation ou d'erreur
    - un status code correspondant
    """

    if updated_parcelle.nom_parcelle is None and updated_parcelle.surface is None and updated_parcelle.coordonnees is None:
        raise HTTPException(status_code=400, detail="Il manque un paramètre")

    all_parcelle = session.query(Parcelle).all()

    if not any(parcelle.no_parcelle == no_parcelle for parcelle in all_parcelle):
        raise HTTPException(status_code=404, detail="Parcelle non trouvé")


    if updated_parcelle.nom_parcelle is not None:
        for parcelle in all_parcelle:
            if parcelle.nom_parcelle == updated_parcelle.nom_parcelle and parcelle.no_parcelle != no_parcelle:
                raise HTTPException(status_code=400, detail="Parcelle déjà existant")

    try:
        parcelle = session.query(Parcelle).filter(Parcelle.no_parcelle == no_parcelle).first()
        if updated_parcelle.nom_parcelle is not None:
            parcelle.nom_parcelle = updated_parcelle.nom_parcelle
        else:
            updated_parcelle.nom_parcelle = parcelle.nom_parcelle
        if updated_parcelle.surface is not None:
            parcelle.surface = updated_parcelle.surface
        else:
            updated_parcelle.surface = parcelle.surface

        if updated_parcelle.coordonnees is not None:
            parcelle.coordonnees = updated_parcelle.coordonnees
        else:
            updated_parcelle.coordonnees = parcelle.coordonnees
        session.commit()
        return {"message": "Parcelle modifié avec succès", "parcelle": updated_parcelle.model_dump()}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))