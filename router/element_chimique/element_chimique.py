from fastapi import APIRouter

router = APIRouter(prefix="/element_chimique", tags=['element_chimique'])
from .methods.create import *