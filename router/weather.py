from fastapi import APIRouter

router = APIRouter(prefix="/weather", tags=['weather'])
from router.methods.create import create_weather
from router.methods.read_data import read_json
from router.methods.patch import modify_weather
from router.methods.put import put_weather