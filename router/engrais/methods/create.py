from database import session
from router.engrais.engrais import router
from models import Engrais
from models import Unite
from pydantic import BaseModel
from fastapi import HTTPException

class EngraisBase(BaseModel):
    un: str
    nom_engrais: str


@router.post("/", status_code=201)
def create_engrais(new_engrais: EngraisBase):
    """
    Ajoute une ligne dans la table engrais
    ### Paramètres
    - engrais: objet de type Engrais, avec les champs un et nom_engrais
    ### Retour
    - Status code 201 si tout s'est bien passé avec message de confirmation
    - Message d'erreur avec le status code correspondant sinon
    """

    engrais = session.query(Engrais).all()
    for engrais_item in engrais:
        if engrais_item.nom_engrais == new_engrais.nom_engrais:
            raise HTTPException(status_code=400, detail="Engrais déjà existant")

    unites = session.query(Unite).all()
    if not any(un.un == new_engrais.un for un in unites):
        raise HTTPException(status_code=404, detail="Unite non trouvée")

    try:
        add_engrais = Engrais(un=new_engrais.un, nom_engrais=new_engrais.nom_engrais)
        session.add(add_engrais)
        session.commit()
        return {"message": "Engrais créé avec succès", "engrais": new_engrais.model_dump()}

    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
