from fastapi import APIRouter

router = APIRouter(prefix="/culture", tags=['culture'])
from .methods.create import *
from .methods.read import *