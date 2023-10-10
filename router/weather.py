from fastapi import APIRouter

router = APIRouter(prefix="/weather", tags=['weather'])
from router.methods.put import put_weather