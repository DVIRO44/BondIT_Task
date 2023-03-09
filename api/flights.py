from fastapi import APIRouter
from typing import Dict, List
from flights_manager import FlightsManager
from schemas import Flight

flights_manager = FlightsManager()
router = APIRouter()


@router.get("/flight_info")
async def get_flight_info(flight_id):
    return flights_manager.get_flight_info(flight_id)


@router.post("/insert_flights")
async def insert_flights(new_flights: List[Flight]):
    return {"Status": flights_manager.determine_flights_status(new_flights=new_flights)}





