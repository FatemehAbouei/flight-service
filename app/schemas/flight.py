# app/schemas/flight.py
from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime

class FlightBase(BaseModel):
    flight_number: str
    origin: str
    destination: str
    departure_time: datetime
    arrival_time: datetime
    duration_minutes: Optional[int]
    aircraft_type: Optional[str]
    seats_total: Optional[int]
    seats_available: Optional[int]
    status: Optional[str]
    process_id: Optional[str]

class FlightCreate(FlightBase):
    flight_id: int = Field(..., description="Unique integer ID for flight")
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None

class FlightUpdate(BaseModel):
    flight_number: Optional[str]
    origin: Optional[str]
    destination: Optional[str]
    departure_time: Optional[datetime]
    arrival_time: Optional[datetime]
    duration_minutes: Optional[int]
    aircraft_type: Optional[str]
    seats_total: Optional[int]
    seats_available: Optional[int]
    status: Optional[str]
    process_id: Optional[str]

class FlightOut(FlightBase):
    flight_id: int
    created_at: Optional[datetime]
    updated_at: Optional[datetime]

    class Config:
        orm_mode = True
