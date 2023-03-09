from pydantic import BaseModel


class Flight(BaseModel):
    flight_ID: str
    Arrival: str
    Departure: str
    success: str = ""
