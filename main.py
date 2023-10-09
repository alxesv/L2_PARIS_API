from typing import Union

from fastapi import FastAPI

app = FastAPI()


@app.get("/")
def read_root():
    return {"Hello": "World"}


@app.get("/items/{item_id}")
def read_item(item_id: int, q: Union[str, None] = None):
    """
    Exemple de docstring pour la fonction read_item
    :param item_id: id de l'item
    :param q: paramètre optionnel
    :return: dict
    """
    return {"item_id": item_id, "q": q}
