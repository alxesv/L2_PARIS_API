from fastapi import APIRouter
from fastapi import FastAPI

router = APIRouter(prefix="/weather", tags=['weather'])

from read_data import read_json

