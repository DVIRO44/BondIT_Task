from fastapi import APIRouter
from api import flights

api_router = APIRouter()
api_router.include_router(flights.router, prefix="/FlightsManager", tags=["FlightsManager"])