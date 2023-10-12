from fastapi import APIRouter

router = APIRouter(prefix="/unite", tags=['unite'])
from .methods.create import *
from .methods.read import *
from .methods.replace import *
from .methods.delete import *