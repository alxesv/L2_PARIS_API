from fastapi import APIRouter
router = APIRouter(prefix="/weather", tags=['weather'])
from create import create_weather