from fastapi import APIRouter

router = APIRouter(prefix="/weather", tags=['weather'])
from router.methods.patch import modify_weather