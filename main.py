from typing import Union

from fastapi import FastAPI

from router.unite.unite import router as unite_router
from router.production.production import router as production_router

app = FastAPI()
app.include_router(unite_router)
app.include_router(production_router)

@app.get("/")
def read_root():
    return {"Hello": "World"}


@app.get("/items/{item_id}")
def read_item(item_id: int, q: Union[str, None] = None):
    return {"item_id": item_id, "q": q}
