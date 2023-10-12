from typing import Union

from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse

from router.unite.unite import router as unite_router
from router.parcelle.parcelle import router as parcelle_router
from router.authentification.authentification import router as authentification_router

from jose import jwt

from dotenv import load_dotenv
import os

load_dotenv()
app = FastAPI()


@app.middleware("http")
async def verify_token(request: Request, call_next):
    """
    used to verify authorization from an http request
    request param = details on the request
    call_next     = call the function next the middleware
    """
    if request.url.path.startswith("/api"):
        # don't verify on route /jwt/
        if request.url.path == "/api/auth/jwt":
            return await call_next(request)
        # try to decode the token if there's one
        if request.headers.get('authorization') is not None:
            try:
                jwt.decode(request.headers.get('authorization'), os.getenv('JWT_SECRET'), algorithms=['HS256'])
            except Exception as e:
                return_message = {
                    "status": 403,
                    "message": "Token de connection invalide",
                    "reason": str(e)
                }
                return JSONResponse(status_code=403, content=return_message)
        else:
            return_message = {
                "status": 401,
                "message": "Aucun token de connexion envoyé",
            }
            return JSONResponse(status_code=401, content=return_message)
        response = await call_next(request)
        return response
    else:
        return await call_next(request)


app.include_router(unite_router, prefix="/api")
app.include_router(parcelle_router, prefix="/api")
app.include_router(authentification_router, prefix="/api")


@app.get("/")
def read_root():
    return {"Hello": "World"}


@app.get("/items/{item_id}")
def read_item(item_id: int, q: Union[str, None] = None):
    return {"item_id": item_id, "q": q}
