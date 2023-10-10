from fastapi import APIRouter, FastAPI
router = APIRouter(prefix="/weather", tags=['weather'])
from create import create_weather
from read_data import read_json
from router.methods.patch import modify_weather
