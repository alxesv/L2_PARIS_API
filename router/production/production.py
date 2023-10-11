from fastapi import APIRouter

router = APIRouter(prefix="/production", tags=['production'])
from .methods.create import *
from .methods.delete import *