from fastapi import APIRouter

router = APIRouter(prefix="/date", tags=['date'])
from .methods.create import *
from .methods.delete import *
from .methods.read import *
from .methods.put import *
from .methods.patch import *