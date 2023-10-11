from fastapi import APIRouter

router = APIRouter(prefix="/production", tags=['production'])
from .methods.create import *
from .methods.delete import *
from .methods.read import *
from .methods.replace import *
from .methods.update import *