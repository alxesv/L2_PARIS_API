from pydantic import BaseModel


class ElementChimiqueBase(BaseModel):
    code_element: str
    un: str
    libelle_element: str


class OptionalElementChimiqueBase(BaseModel):
    code_element: str | None
    un: str | None
    libelle_element: str | None