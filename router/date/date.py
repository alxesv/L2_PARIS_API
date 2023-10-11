from fastapi import APIRouter

router = APIRouter(prefix="/date", tags=['date'])
from .methods.create import *
from .methods.delete import *
from .methods.past import *
from .methods.put import *
from .methods.read import *